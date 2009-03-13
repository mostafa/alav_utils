#! /usr/bin/env python
#-----------------------------------------------------------------------
#       repo_maker  Version           $$VERSION$$
#       By :
#                  Sameer Rahmani <lxsameer@gmail.com> 
#       Home :
#                  $$HOME$$
#-----------------------------------------------------------------------

import os , sys
import subprocess as SB
from  sps.term import *
from  optparse import OptionParser

#+++++++++++++++++++++++++++++++++++++++
# Requerment :
#  * A debian based linux box .
#  * apt-move
#  * apt-rdepends
#+++++++++++++++++++++++++++++++++++++++

def apt_clean ():
    
    twrite ("\nCleaning cache archive . . ." , "WHITE")
    try:
        SB.check_call (['apt-get' , 'clean'])
        status ("OK" , 0)
    except:
        twrite ("\nError : Can not clean the /var/cache/apt/archives/ .\n" , "BRED")
        sys.exit(1)

def process_package_list (path):
    if path[-1:] != "/":
        path = path + "/"
    twrite ("Processing packages list . . ." , "WHITE")
    try:
        fd = open (path + "Packages_list" , "r")
    except :
        status ("Faild" , -1)
        twrite ("Error : \"%s\" No such file or permission denied !\n" % (path + "Packages_list") , "BRED" )
        sys.exit (1)
    status ("OK" , 0)
    tmp = fd.readlines()
    plist = []
    for i in tmp:
        if i != '\n' :
            i = i.replace ("\n" , "")
            plist.append (i)

    return plist


def apt_rdepends (plist):
    apt = ['apt-rdepends'] + plist
    output = SB.Popen (apt , stdout=SB.PIPE).communicate ()[0]
    deplist = output.split ("\n")
    #!!!
    # here i should check other value like pre depend or others that i don't know
    #!!!
    dlist = []
    for i in deplist:
        if (i.find ("Depends") > 0) or (i.find ("PreDepends") > 0):
            a = i.split(":")[1].split (" ")[1]
            dlist.append (a)
    return dlist
        

def aptitude (param , plist):
    ### maybe i should find a better way for analyze the virtual package.
    rdlist  = []
    apt = ['aptitude'] + param + plist
    output = SB.Popen (apt , stdout=SB.PIPE).communicate ()[0]
    alist = output.split ("\n")
    vlst = []
    plst = []
    c = 0
    for i in alist:
        if len (i) > 0:
            
            if i[0] == "v":
                a = i.split (" ")
                
                for j in a:
                    if len(j) > 2:
                        
                        if j in plist:
                            vlst.append (j.strip ())
                            while 1:
                                try:
                                    plist.pop(plist.index(j))
                                except:
                                    break
            
                
    return vlst , plist





def aptitude_show (plist):
    apt = ['aptitude' , 'show'] + plist
    output = SB.Popen (apt , stdout=SB.PIPE).communicate ()[0]
    alist = output.split ("\n")
    lst = []
    
    for i in alist:
        
        if i.find("Provided") == 0:
            
            a = i.split (":")[1].strip ()
            try:
                c = a.split (",")
            except:
                c = [a]
            
            for j in c:
                lst.append (j.strip ())
    return lst



def aptitude_download (args , plist , verbose = False):
    apt = ['aptitude'] + args + plist
    pwd = os.getcwd ()
    os.chdir ('/var/cache/apt/archives/')
    
    twrite ("Downloading pool packages . . ." , "WHITE")
    try:
        
        output = SB.Popen (apt , stdout = SB.PIPE ).communicate ()[0]
        
        os.chdir(pwd)

    except:    
        status ("Faild" , -1)
        twrite ("Check your apt configuration and your connection .\n" , "BROWN")
        os.chdir(pwd)
        sys.exit (1)
    status ("OK" , 0 )
    if verbose :
        print output
    
def apt_move (dest , dist , gpgkey):
    apt = ['apt-move'  , '-c' ,  './apt_move.conf' , 'update']
    tmp = "APTSITES=\"/all/\"\nLOCALDIR=%s\nDIST=%s\nPKGTYPE=binary\nFILECACHE=/var/cache/apt/archives\nGPGKEY=%s\n" % (dest , dist , gpgkey)
    twrite ("Crearing pool directory . . ." , "WHITE")
    fd = open ('apt_move.conf' , 'w+')
    fd.write (tmp)
    fd.close ()
    output = ""
    try:
        output = SB.Popen (apt , stdout=SB.PIPE).communicate ()[0]
    except:
        status ("Faild" , -1)
        
        os.unlink ('./apt_move.conf')
        sys.exit (1)
    os.unlink ('./apt_move.conf')
    status ("OK" , 0)

        
    



def main (dest , dist , gpgkey , verbose):
    apt_clean ()

    plist = process_package_list (dest)
    
    dlist = apt_rdepends (plist)
    
    virtual_dlist , rdlist = aptitude (["search" ,] , dlist)
    
    rvlist = aptitude_show (virtual_dlist) 
    
    rdlist.extend (rvlist)
    
    aptitude_download (["download" ] , rdlist , verbose)
    
    apt_move (dest , dist , gpgkey)

    ###
    #  I should add a Release file modifier.
    ###





if __name__ == "__main__":


    if (os.getuid () != 0):
        twrite ( "Error : I need root privilege to do my action.\n" , "BRED")
        sys.exit(1)

    parser = OptionParser ()
    
    parser.add_option ("-d" , "--dest" , dest="dest" , metavar="PATH" , help="Set the destination PATH for creating repository." , default="./")
    parser.add_option ("-v" , "--verbose" , dest="verbose" , help="Show more details." , action="store_true" , default=False)
    parser.add_option ("-g" , "--gpg-key" , dest="gpgkey" , help="Sign the deb Packages by KEY" , metavar="KEY" , default="")

    parser.add_option ("-n" , dest="dist" , metavar="CODENAME" , help="build the repository with CPDENAME" ,default="testing")


    option , args = parser.parse_args()

    dest = option.dest
    dist = option.dist
    gpgkey = option.gpgkey



    try:
        stat = os.stat (dest)
    except:
        twrite ("Error : \"%s\" no such file or directory . \n" % stat , "BRED" )
        sys.exit(1)

#    try:
        
    twrite ("\n\nNOTE" , "CYAN")
    twrite (" : " , "WHITE")
    twrite ("Please read the README file before using this tool .\n\n" , "BGREEN")

    
    twrite ( "Press any key to continue.\n" , "WHITE")
    
    getch ()
    main (os.path.abspath (dest) ,dist , gpgkey ,  option.verbose)        
 #   except:
 #       pass
