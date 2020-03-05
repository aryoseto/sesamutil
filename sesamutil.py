"""sesamutil.py: Bunch of SESAM utility tools"""

__author__      = "Aryo Wicaksono - Ramzitech"
__copyright__   = "Copyright 2020, Ramzitech"
__version__ = "0.0.1"

import itertools


def getForceDisp(filename, selection) :
    ''' Open SPLICE.LIS file and screen the disp and force
        Selection: "d" = displacement
                   "f" = force '''
    with open(filename, 'r') as toread :
        outlist = []
        readstatus = False  #indicator of taking the data
        notlinearstatus = True #indicator of finding the linearised results 
        for line in toread :
            
            #Get load case number
            if 'to generate equivalent linear' in line :
                notlinearstatus = False
            
            if 'LOAD VECTOR NUMBER'in line :
                femloadnum = line.split('=')[1].strip()
                notlinearstatus = True

            #Screen anything that has 11 items for each line
            if ( len(line.split()) == 11 and readstatus == True and notlinearstatus == True 
                    and is_number(line.split()[5])
                    and is_number(line.split()[3]) ):
                
                outlist.append(femloadnum + '  ' + line)

            if selection == 'd' :
                if "PILE HEAD GLOBAL RESULTING DISPLACEMENTS" in line :
                    readstatus = True
                elif "PILE HEAD GLOBAL RESULTING FORCES" in line :
                    readstatus = False
            
            elif selection == 'f' :
                if "PILE HEAD GLOBAL RESULTING DISPLACEMENTS" in line :
                    readstatus = False
                elif "PILE HEAD GLOBAL RESULTING FORCES" in line :
                    readstatus = True

    return outlist


def getPileName(filename) :
    '''Find all the pile names including its splice name, reading the SPLICE.LIS file'''
    with open(filename, 'r') as toread:
        
        pilelist = {}
        readstatus = False
        for line in toread :
            if readstatus == True :
                if len(line.split()) == 2:
                    pilelist[line.split()[0]] = line.split()[1]
                else :
                    readstatus = False    
    
            if "PILE CONCEPT NAME" in line :
                readstatus = True
    
    return pilelist


def writeFile(listname, outfilename) :
    with open(outfilename, 'w') as outfile:
        for line in listname :
            outfile.write(line)


def is_number(astring):
    ''' to check whether string is a number format '''
    try:
        float(astring)
        return True
    except ValueError:
        return False

def getFatRes(filename) :
    ''' Extracting fatigue analysis results from framework'''
    with open(filename, 'r') as toread :
        outlist = []
        outdict = {}
        
        newjointstatus = True
        newbracestatus = True

        counter = 0

        for num, line in enumerate(toread) :

            
            if is_number(line[65:73].strip()) :
                #counter = counter + 1
                
                # FIRST LINE
                if len(line[35:].split()) == 9 :
                    indicator =  1

                    if len(line[:9].strip()) != 0 :
                        jointno =  line[:9].strip()

                    if len(line[10:22].strip()) !=0:
                        braceno = line[10:22].strip()
                    
                    damage, life, side, hotspot, scfrule, scfax, scfipb, scfopb, sncurve = line[35:].split()
                
                # SECOND LINE
                elif len(line[35:].split()) == 8 and indicator == 1 :
                    indicator = indicator + 1
                    
                    if len(line[10:22].strip()) != 0 :
                        chordno = line[10:22].strip()

                    alpha, symmet, bracedia, bracethk, gap, thifac, qr, cycles = line[45:].split()

                # THIRD LINE
                elif len(line[35:].split()) == 8 and indicator == 2 :
                    indicator = indicator + 1
                    
                    theta, jotype, chorddia, chordthk, lencho, fixcho, scfaxc, scfaxs = line[45:].split()


                # Store the parameters
                if indicator == 3 :
                    outlist.append([jointno, braceno, chordno, side, hotspot, scfax, scfipb, scfopb, scfaxc, scfaxs,
                                   sncurve, scfrule, alpha, theta, symmet, bracedia, bracethk, chorddia, chordthk,
                                    jotype,  lencho, fixcho, gap, thifac, qr, cycles, damage, life, ])
                    
                    #outlist.append([jointno, braceno, side, life])

                #print(counter)

    return outlist




if __name__ == "__main__":
    ''' Test '''
    #SPLICE
    #rawstuff = getForceDisp("SPLICE.LIS", 'd')
    #print("first 10 lines : \n", *rawstuff[3050:3090], sep='/n')

    #pilename = getPileName("SPLICE.LIS")
    #print("pile names :", pilename)

    #Fatigue framework
    #fatiguelist = getFatRes('SABFTG_UNSTIFFENED.LIS')
    #print(*fatiguelist[:50], sep='\n')
    #fatiguedict = getFatRes('SABFTG_UNSTIFFENED.LIS')
    #print(fatiguedict['JT106'])
    #print(dict(itertools.islice(fatiguedict.items(), 1)))

    fatiguelist = getFatRes('SABFTG_UNSTIFFENED.LIS')
    print(*fatiguelist[:2], sep='\n')