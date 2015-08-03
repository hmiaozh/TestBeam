# Test beam code instructions 

## Setup the code

This is meant for machines wich access to CMSSW (e.g. lxplus)

```
cmsrel CMSSW_7_5_0
cd CMSSW_7_5_0/src
git init
## use the ssh repo link if you are going to make commits 
git remote add origin https://github.com/BaylorCMS/cmssw.git
git config core.sparsecheckout true
echo "DataFormats/HcalDigi/" > .git/info/sparse-checkout
echo "EventFilter/HcalRawToDigi/" >> .git/info/sparse-checkout
echo "RecoTBCalo/HcalTBObjectUnpacker/" >> .git/info/sparse-checkout
echo "UserCode/" >> .git/info/sparse-checkout
## uncomment branch you are interested in
#git pull origin HcalTestBeam
git pull origin HcalTestBeamQIE11
```

If you want to bring your checkout up to date with the main repo, just repeat the last step
```
#git pull origin HcalTestBeam
git pull origin HcalTestBeamQIE11
```

## Instructions on how to use the code

First make sure to compile
```
scram b
cmsenv
```

Note that `configQADCTDC.txt` should be in `[your_destination_directory]/CMSSW_7_5_0/src`
This file is read during cmsRun.

Go to the directory containing the analyzer code
```
cd UserCode/H2TestBeamAnalyzer
```

This directory should contain:

1. An EMAP:
  - EMAP_H2_Arjan_PhiFix.txt : current test beam emap, which is read during cmsRun
  - EMAP_b28.txt : current emap for the setup in b28, contains the QIE11 information
2. testbeam data file (e.g.  HTB_007824.root, which originally came from cmshcaltb02.cern.ch:/data/spool/HTB_007824.root)

Now we are ready for cmsRun:

#### For the general test beam setup:

```
## The first argument is the run number, prepended with zeroes to match the filename.
cmsRun h2testbeamanalyzer_cfg.py 007824 > run_007824.log
```
This cmsRun step will generate a file of the form ana_h2_tb_run007824.root, 
which can be inspected with e.g. ROOT TBrowser.

For a lot of diagnostic digi output from cmsRun, use `h2testbeamanalyzer_cfg_verbose.py`

Run the following scripts to create histograms from ana_h2_tb_run007824.root:

```
# Process the file:
./tb_ana.py --i ana_h2_tb_run007824.root --o ana_tb_out_run7824.root --r 7824 

# Make plots
./tb_plots.py --i ana_tb_out_run7824.root --o tb_plots_run7824 --r 7824 
```

Then, in principle one can use
```
./makeHtml.py tb_plots_run7824
```
to prepare the plots for a webpage.  However, this step seems to have 
problems if one has already used cmsenv on lxplus.  It seems to
work in a new shell in which cmsenv has not been used.

At this point, the contents of tb_plots_run7824 should be suitable for use with a web server, if you have some place to copy the files.
If not, it is possible to look at files directly using display (e.g. "display *pdf") in a shell where you have not already used cmsenv.
One can see the plots from this run here:  http://hep.baylor.edu/cmshcal/HcalTestBeam/tb_plots_run7824

####For the setup in B28, containing the QIE11

```
## Update this file to point to your data file
cmsRun h2testbeamanalyzer_cfg_b28.py > b28.log
```

This wil create a file ana_h2_tb_run_b28.root, which can be inspected with e.g. ROOT TBrowser. 

Run the following scripts to create histograms from ana_h2_tb_run_b28.root:

```
# Process the file:
./tb_qie_ana.py -i ana_h2_tb_run_b28.root -o ana_tb_out_run_b28.root -n <nevents> 

# Make plots; run number is used to name output root file
./tb_qie_plots.py -i ana_tb_out_run_b28.root -o tb_plots_run8 -r 8
```

As above, the plots can be prepared for web viewing via
```
./makeHtml.py tb_plots_run8
```
