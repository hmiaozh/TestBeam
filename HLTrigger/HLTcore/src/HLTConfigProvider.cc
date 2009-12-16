/** \class HLTConfigProvider
 *
 * See header file for documentation
 *
 *  $Date: 2009/12/16 10:29:41 $
 *  $Revision: 1.12 $
 *
 *  \author Martin Grunewald
 *
 */

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <iostream>

void HLTConfigProvider::clear()
{
   using namespace std;
   using namespace edm;

   // clear data members

   processName_ = "";
   registry_    = pset::Registry::instance();

   processPSet_   = ParameterSet();

   tableName_   = "/dev/null";

   triggerNames_.clear();
   moduleLabels_.clear();

   triggerIndex_.clear();
   moduleIndex_.clear();

   pathNames_.clear();
   endpathNames_.clear();

   prescaleLabels_.clear();
   prescaleIndex_.clear();
   prescaleValues_.clear();

}

bool HLTConfigProvider::init(const edm::Event& iEvent, const std::string& processName, bool& changed)
{
   using namespace std;
   using namespace edm;

   LogDebug("HLTConfigProvider") << "Called with processName '"
				 << processName << "'." << endl;

   ParameterSet eventPSet;
   if (iEvent.getProcessParameterSet(processName,eventPSet)) {
     if ( processPSet_==eventPSet ) {
       changed=false;
     } else { 
       clear();
       processName_  =processName;
       processPSet_  =eventPSet;
       LogDebug("HLTConfigProvider") << "New ProcessPSet!";
       LogDebug("HLTConfigProvider") << processPSet_;
       extract();
       changed=true;
     }
     return true;
   } else {
     clear();
     LogError("HLTConfigProvider")
       << "Event ProcessPSet not found for processName '"
       << processName <<"'!";
     changed=true;
     return false;
   }

}

bool HLTConfigProvider::init(const std::string& processName)
{
   using namespace std;
   using namespace edm;

   LogError("HLTConfigProvider")
     << " Called with deprecated init(processName) method - "
     << " Must call init(iEvent,processName) each event!";

   LogDebug("HLTConfigProvider") << "Called with processName '"
				 << processName << "'." << endl;

   // initialise
   clear();

   // Obtain ParameterSetID for requested process (with name
   // processName) from pset registry
   string pNames("");
   ParameterSet   pset;
   ParameterSetID psetID;
   unsigned int   nPSets(0);
   for (edm::pset::Registry::const_iterator i = registry_->begin(); i != registry_->end(); ++i) {
     if (i->second.exists("@process_name")) {
       const std::string pName(i->second.getParameter<string>("@process_name"));
       pNames += pName+" ";
       if ( pName == processName ) {
	 psetID = i->first;
	 nPSets++;
       }
     }
   }

   LogDebug("HLTConfigProvider") << "Unordered list of process names found: "
				 << pNames << "." << endl;

   if (nPSets==0) {
     LogError("HLTConfigProvider") << " Process name '"
				   << processName
				   << "' not found in registry!" << endl;
     return false;
   }
   if (psetID==ParameterSetID()) {
     LogError("HLTConfigProvider") << " Process name '"
				   << processName
				   << "' found but ParameterSetID invalid!"
				   << endl;
     return false;
   }
   if (nPSets>1) {
     LogError("HLTConfigProvider") << " Process name '"
				   << processName
				   << " found " << nPSets
				   << " times in registry!" << endl;
     return false;
   }

   // Obtain ParameterSet from ParameterSetID
   if (!(registry_->getMapped(psetID,pset))) {
     LogError("HLTConfigProvider") << " ProcessPSet for ProcessPSetID '"
				   << psetID
				   << "' not found in registry!" << endl;
     return false;
   }

   processName_=processName;
   processPSet_=pset;
   extract();
   LogDebug("HLTConfigProvider") << "ProcessPSet:";
   LogDebug("HLTConfigProvider") << processPSet_;

   return true;

}

void HLTConfigProvider::extract()
{
   using namespace std;
   using namespace edm;

   // Obtain PSet containing table name (available only in 2_1_10++ files)
   if (processPSet_.exists("HLTConfigVersion")) {
     const ParameterSet HLTPSet(processPSet_.getParameter<ParameterSet>("HLTConfigVersion"));
     if (HLTPSet.exists("tableName")) {
       tableName_=HLTPSet.getParameter<string>("tableName");
     }
   }
   LogInfo("HLTConfigProvider") << " HLT-ConfDB TableName = '"
				<< tableName_
				<< "'." << endl;

   // Extract trigger paths, which are paths but with endpaths to be
   // removed, from ParameterSet
   pathNames_   = processPSet_.getParameter<vector<string> >("@paths");
   endpathNames_= processPSet_.getParameter<vector<string> >("@end_paths");
   const unsigned int nP(pathNames_.size());
   const unsigned int nE(endpathNames_.size());
   for (unsigned int iE=0; iE!=nE; ++iE) {
     const std::string& endpath(endpathNames_[iE]);
     for (unsigned int iP=0; iP!=nP; ++iP) {
       if (pathNames_[iP]==endpath) {
	 pathNames_[iP]=""; // erase endpaths
       }
     }
   }
   triggerNames_.reserve(nP);
   for (unsigned int iP=0; iP!=nP; ++iP) {
     if (pathNames_[iP]!="") {triggerNames_.push_back(pathNames_[iP]);}
   }
   pathNames_   = processPSet_.getParameter<vector<string> >("@paths");

   // Obtain module labels of all modules on all trigger paths
   const unsigned int n(size());
   moduleLabels_.reserve(n);
   for (unsigned int i=0;i!=n; ++i) {
     moduleLabels_.push_back(processPSet_.getParameter<vector<string> >(triggerNames_[i]));
   }

   // Fill index maps for fast lookup
   moduleIndex_.resize(n);
   for (unsigned int i=0; i!=n; ++i) {
     triggerIndex_[triggerNames_[i]]=i;
     moduleIndex_[i].clear();
     const unsigned int m(size(i));
     for (unsigned int j=0; j!=m; ++j) {
       moduleIndex_[i][moduleLabels_[i][j]]=j;
     }
   }

   // Extract and fill PrescaleService information
   prescaleValues_.resize(n);
   for (unsigned int i=0; i!=n; ++i) {
     prescaleValues_[i].clear();
   }
   if (processPSet_.exists("PrescaleService")) {
     const edm::ParameterSet PSet (modulePSet("PrescaleService"));
     prescaleLabels_ = PSet.getParameter< std::vector<std::string> >("lvl1Labels");
     const unsigned int m(prescaleLabels_.size());
     for (unsigned int j=0; j!=m; ++j) {
       prescaleIndex_[prescaleLabels_[j]]=j;
     }

     prescaleValues_.resize(n);
     for (unsigned int i=0; i!=n; ++i) {
       prescaleValues_[i].resize(m);
       for (unsigned int j=0; j!=m; ++j) {
	 prescaleValues_[i][j]=1;
       }
     }

     const edm::VParameterSet VPSet(PSet.getParameter<edm::VParameterSet>("prescaleTable"));
     const unsigned int l(VPSet.size());
     for (unsigned int j=0; j!=l; ++j) {
       const unsigned int i(triggerIndex(VPSet[j].getParameter<std::string>("pathName")));
       if (i<size()) {
	 prescaleValues_[i]=VPSet[j].getParameter<std::vector<unsigned int> >("prescales");
       }
     }

   }

   return;
}

void HLTConfigProvider::dump (const std::string& what) const {
   using namespace std;
   using namespace edm;

   if (what=="processName") {
     cout << "HLTConfigProvider::dump: ProcessName = " << processName_ << endl;
   } else if (what=="ProcessPSet") {
     cout << "HLTConfigProvider::dump: ProcessPSet = " << endl << processPSet_ << endl;
   } else if (what=="TableName") {
     cout << "HLTConfigProvider::dump: TableName = " << tableName_ << endl;
   } else if (what=="Triggers") {
     const unsigned int n(size());
     cout << "HLTConfigProvider::dump: Triggers: " << n << endl;
     for (unsigned int i=0; i!=n; ++i) {
       cout << "  " << i << " " << triggerNames_[i] << endl;
     }
   } else if (what=="Modules") {
     const unsigned int n(size());
     cout << "HLTConfigProvider::dump Triggers and Modules: " << n << endl;
     for (unsigned int i=0; i!=n; ++i) {
       const unsigned int m(size(i));
       cout << i << " " << triggerNames_[i] << " " << m << endl;
       cout << " - Modules: ";
       unsigned int nHLTPrescalers(0);
       unsigned int nHLTLevel1GTSeed(0);
       for (unsigned int j=0; j!=m; ++j) {
	 const string& label(moduleLabels_[i][j]);
	 const string  type(moduleType(label));
	 cout << " " << j << ":" << label << "/" << type ;
	 if (type=="HLTPrescaler") nHLTPrescalers++;
	 if (type=="HLTLevel1GTSeed") nHLTLevel1GTSeed++;
       }
       cout << endl;
       cout << " - Number of HLTPrescaler/HLTLevel1GTSeed modules: " 
	    << nHLTPrescalers << "/" << nHLTLevel1GTSeed << endl;
     }
   } else {
     cout << "HLTConfigProvider::dump: Unkown dump request: " << what << endl;
   }
   return;
}

unsigned int HLTConfigProvider::size() const {
  return triggerNames_.size();
}
unsigned int HLTConfigProvider::size(unsigned int trigger) const {
  return moduleLabels_.at(trigger).size();
}
unsigned int HLTConfigProvider::size(const std::string& trigger) const {
  return size(triggerIndex(trigger));
}

const std::string& HLTConfigProvider::tableName() const {
  return tableName_;
}
const std::vector<std::string>& HLTConfigProvider::triggerNames() const {
  return triggerNames_;
}
const std::string& HLTConfigProvider::triggerName(unsigned int trigger) const {
  return triggerNames_.at(trigger);
}
unsigned int HLTConfigProvider::triggerIndex(const std::string& trigger) const {
  const std::map<std::string,unsigned int>::const_iterator index(triggerIndex_.find(trigger));
  if (index==triggerIndex_.end()) {
    return size();
  } else {
    return index->second;
  }
}

const std::vector<std::string>& HLTConfigProvider::moduleLabels(unsigned int trigger) const {
  return moduleLabels_.at(trigger);
}
const std::vector<std::string>& HLTConfigProvider::moduleLabels(const std::string& trigger) const {
  return moduleLabels_.at(triggerIndex(trigger));
}

const std::string& HLTConfigProvider::moduleLabel(unsigned int trigger, unsigned int module) const {
  return moduleLabels_.at(trigger).at(module);
}
const std::string& HLTConfigProvider::moduleLabel(const std::string& trigger, unsigned int module) const {
  return moduleLabels_.at(triggerIndex(trigger)).at(module);
}

unsigned int HLTConfigProvider::moduleIndex(unsigned int trigger, const std::string& module) const {
  const std::map<std::string,unsigned int>::const_iterator index(moduleIndex_.at(trigger).find(module));
  if (index==moduleIndex_.at(trigger).end()) {
    return size(trigger);
  } else {
    return index->second;
  }
}
unsigned int HLTConfigProvider::moduleIndex(const std::string& trigger, const std::string& module) const {
  return moduleIndex(triggerIndex(trigger),module);
}

const std::string HLTConfigProvider::moduleType(const std::string& module) const {
  if (processPSet_.exists(module)) {
    return modulePSet(module).getParameter<std::string>("@module_type");
  } else {
    return "";
  }
}

const edm::ParameterSet& HLTConfigProvider::processPSet() const {
  return processPSet_;
}

const edm::ParameterSet HLTConfigProvider::modulePSet(const std::string& module) const {
  if (processPSet_.exists(module)) {
    return processPSet_.getParameter<edm::ParameterSet>(module);
  } else {
    return edm::ParameterSet();
  }
}

/*
const std::vector<std::string>& HLTConfigProvider::prescaleLabels() const {
  return prescaleLabels_;
}

const std::string& HLTConfigProvider::prescaleLabel(unsigned int label) const {
  return prescaleLabels_.at(label);
}

unsigned int HLTConfigProvider::prescaleIndex(const std::string& label) const {
  const std::map<std::string,unsigned int>::const_iterator index(prescaleIndex_.find(label));
  if (index==prescaleIndex_.end()) {
    return prescaleLabels_.size();
  } else {
    return index->second;
  }
}

const std::vector<unsigned int>& HLTConfigProvider::prescaleValues(unsigned int trigger) const {
  return prescaleValues_.at(trigger);
}

const std::vector<unsigned int>& HLTConfigProvider::prescaleValues(const std::string& trigger) const {
  return prescaleValues(triggerIndex(trigger));
}

unsigned int HLTConfigProvider::prescaleValue(unsigned int trigger, unsigned int label) const {
  return prescaleValues(trigger).at(label);
}

unsigned int HLTConfigProvider::prescaleValue(const std::string& trigger, const std::string& label) const {
  return prescaleValue(triggerIndex(trigger),prescaleIndex(label));
}
*/
