import os

class HTMLGenerator:

    def exportToHTML(self,data,file):
        fichier=open(file,"w")
        html = "<html><head><title>test</title><meta http-equiv=\"refresh\" content=\"2\"></head><body>"+str(data)+"</body></html>"
        fichier.write(html)
        fichier.close()
