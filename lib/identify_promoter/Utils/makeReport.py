import json
import sys
import matplotlib
import matplotlib.pyplot as plt
from pyseqlogo.pyseqlogo import draw_logo, setup_axis

#Args - 1 - input file_path
#       2 - output file_name(path is hardcoded for now...)
#maybe need to import matplotlib and pyplot?
htmlDir = '/kb/module/work/tmp/html'
htmlReport = '<html><body>'
htmlReport += '<table style="width:100%">\n' + '<tr>\n'
htmlReport += '<th> Sequence </th>\n' + '<th> Logo </th>\n' + '<th> Ratio </th>\n + </tr>\n'
with open(sys.argv[1],'r') as jsonFile:
    jsonData = json.load(jsonFile)
    for motif in jsonData:
        htmlReport += '<tr>\n <td> ' + motif['Iupac_signature'] + ' </td>\n'
        #plt.rcParams['figure.dpi'] = 300
        fig, axarr = draw_logo(motif['pwm'])
        fig.tight_layout()
        imgName = motif['Iupac_signature'] + '_gibbs.png'
        saveTo = htmlDir + '/' + imgName
        htmlReport += '<td> <img src="' + imgName + '"> </td>\n'
        htmlReport += '<td> 1 </td>\n'
        htmlReport += '</tr>\n'
        plt.savefig(saveTo)
        plt.close()
htmlReport += '</table>\n'
htmlReport += '</body></html>'
#htmlPath = htmlDir + '/' + sys.argv[2]
with open(sys.argv[2],'w') as html_handle:
    html_handle.write(str(htmlReport))
