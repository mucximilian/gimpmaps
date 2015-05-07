import os

result_dir = ( "/media/data/daten/studium/master/module/master_thesis/data" 
        + "/rendering/results/"
        + "index.html")

out_dir = ( "/media/data/daten/studium/master/module/master_thesis/data" 
        + "/rendering/results/test/"
        + "index.html")

os.system("cp %s %s" % (
                          result_dir,
                          out_dir
                          )
          )