//#include <vector>
//#include <string>

#define NUMCHS 300
#define NUMTS 50

struct TCalibLedInfo
{
    int numChs;
    int iphi[NUMCHS];
    int ieta[NUMCHS];
    int cBoxChannel[NUMCHS];
    //std::vector<std::string> cBoxString;
    int nTS[NUMCHS];
    double pulse[NUMCHS][NUMTS];
};

struct TQIE8Info
{
    int numChs;
    int numTS;
    int iphi[NUMCHS];
    int ieta[NUMCHS];
    int depth[NUMCHS];
    double pulse[NUMCHS][NUMTS];
    double pulse_adc[NUMCHS][NUMTS];
    double ped[NUMCHS];
    double ped_adc[NUMCHS];
    bool valid[NUMCHS];
};

struct TQIE11Info
{
    int numChs;
    int numTS;
    int iphi[NUMCHS];
    int ieta[NUMCHS];
    int depth[NUMCHS];
    double pulse[NUMCHS][NUMTS];
    double ped[NUMCHS];
    double pulse_adc[NUMCHS][NUMTS];
    double ped_adc[NUMCHS];
    bool capid_error[NUMCHS];
    bool link_error[NUMCHS];
    bool soi[NUMCHS][NUMTS];
};

struct H2Triggers
{
    //
    //  Standard Triggers
    //
    int ped;
    int led;
    int laser;
    int beam;
    //std::string str;

    //
    //  Added for completeness
    //
    int fakeTrg;
    int inSpillTrg;
};

struct H2BeamCounters
{
    double cer1adc;
    double cer2adc;
    double cer3adc;
    double s1adc;
    double s2adc;
    double s3adc;
    double s4adc;
};

struct H2Timing
{
    int s1Count;
    int s2Count;
    int s3Count;
    int s4Count;

    double triggerTime;
    double ttcL1Atime;
};
