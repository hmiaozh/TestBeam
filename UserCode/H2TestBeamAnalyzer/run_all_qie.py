import sys, os

if len(sys.argv) < 2:
    print "Please provide a run number."
    sys.exit()

runnr = sys.argv[1]
runnumber = runnr.rjust(6, "0")

# Run the unpacker etc
print "Run unpacker and QIE11Analzer"
command1 = "cmsRun h2testbeamanalyzer_cfg_qie11.py %s" % (runnumber)
os.system(command1)
print "Make histograms" 
command2 = "python tb_qie_ana.py -i ana_h2_tb_run%s.root -o ana_tb_out_run%s.root" % (runnumber, runnumber)
os.system(command2)
print "Make plots"
command3 = "python tb_qie_plots.py -i ana_tb_out_run%s.root -o plots_run%s -r %s" % (runnumber, runnumber, runnumber.lstrip("0"))
os.system(command3)
print "Make HTML version"
command4 = "python makeHtml.py plots_run%s" % (runnumber)
os.system(command4)
print "Copy to www folder"
command5 = "cp -r plots_run%s /hcalTB/Nadja/" % (runnumber)
os.system(command5)

print "DONE"
