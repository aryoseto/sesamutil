"""sesamutil.py: Bunch of SESAM utility tools"""

__author__      = "Aryo Wicaksono - Ramzitech"
__copyright__   = "Copyright 2020, Ramzitech"
__version__ = "0.0.1"

import itertools
import xlsxwriter


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

def slices(line, listofcolpos):
    position = 0
    outlist = []
    for col in listofcolpos:
        outlist.append(line[position:position + col ].strip())
        position += col
    return outlist


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

def getmemcodecheck(filename) :
    ''' Member code check results from frameworks, FULL  '''
    
    #Extracting data
    outlist = []
    with open(filename, 'r') as toread :
        for line in toread :
            #Screening the select only lines with data
            if is_number(line[118:127].strip()) :
                #First line
                if len(line.split()) == 14 :
                    firstline = line.strip()
                elif len(line.split()) == 11 :
                    secondline = line .strip()
                else :
                    thirdline = line.strip()
                    completeline = firstline.split() + secondline.split() + thirdline.split()
                    
                    outlist.append(completeline)
    
    #Extract headers
    with open(filename, 'r') as toread :
        for line in toread :
            #First line
            if len(line.split()) == 14 and line.split()[0] == "Member" :
                firstline = line.strip()
            elif len(line.split()) == 11 and line.split()[0] == "Phase" :
                secondline = line.strip()
            elif len(line.split()) == 8 and line.split()[0] == "UsfaM" :
                thirdline = line.strip()
                completeheader = firstline.split() + secondline.split() + thirdline.split()
                break

    # Adding header to the top of the list
    outlist.insert(0, completeheader)

    return outlist

def getjointcheckiso(filename) :
    
    #Extracting data
    outlist = []
    with open(filename, 'r') as toread :
        for line in toread :
            templist = slices(line,[9, 9, 9, 4, 9, 10, 8, 10, 10, 10, 10, 9, 7, 9] )
            if is_number(templist[6]) :
                #Identifying first line
                if templist[0] != '' and  templist[1] != '' :
                    firstline = templist

                #Identifying second line
                elif templist[0] == '' and templist[1] != '' :
                    secondline = templist

                #Last line
                else :
                    thirdline = templist
                    comleteline =  [ *firstline ] + [ secondline[1] ] + [ secondline[2] ] + [ *secondline[6:] ] + [ *thirdline[6:] ]
                    outlist.append(comleteline)
    
    header1 = "Joint    Brace    LoadCase CND Jnt/Per  Outcome   Usfac     PB       MBipb     MBopb      Ub       Qup     Qfp   L(a,b,c)"
    header2 = "         Chord     Phase                          UsfaP     Pd       Mdipb     Mdopb     Theta    Quipb   Qfipb   CanFact"
    header3 = "                                                  UsfaM  Method       Fyc     gammaRj     Gap     Quopb   Qfopb     d/D"

    completeheader = header1.split() + header2.split() + header3.split()
    outlist.insert(0, completeheader)

    return outlist

def getconecheckapi(filename) :
    
    #Extracting data
    outlist = []
    with open(filename, 'r') as toread :
        for line in toread :
            templist = slices(line,[9, 9, 5, 8, 9, 9, 9, 10, 10, 10, 10, 9] )
            if is_number(templist[6]) :
                #Identifying first line
                if templist[0] != '' and  templist[1] != '' :
                    firstline = templist

                #Identifying second line
                elif templist[0] == '' and templist[3] != '' :
                    secondline = templist

                #Last line
                else :
                    thirdline = templist
                    comleteline =  [ *firstline ] + [ secondline[1] ] + [ secondline[3] ] + [ *secondline[6:] ] + [ thirdline[6] ] + [ thirdline[7] ] + [ *thirdline[10:] ]
                    outlist.append(comleteline)
    
    header1 = " Member   LoadCase CND Type     Joint/Po Outcome  Usfact    Yield    Tensile    Dummy      fc        fbm"
    header2 = "           Phase       SctNam                     Usfcon     Dia        t        tc        fb        fhm"
    header3 = "                                                  Usfcyl    alpha                         ftot       Fhc"

    completeheader = header1.split() + header2.split() + header3.split()
    outlist.insert(0, completeheader)

    return outlist


def list_to_excel(listname, excelname):
    '''listname and excelname (including the extension, as string) '''
    workbook = xlsxwriter.Workbook(excelname)
    worksheet = workbook.add_worksheet()

    #Start of rows and column
    row = 0
    for line in listname :
        col = 0
        for item in line :
            if is_number(item) :
                worksheet.write_number(row, col, float(item))
            else:
                worksheet.write(row, col, item)
            col += 1
        row +=1

    workbook.close()



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

    #fatiguelist = getFatRes('SABFTG_UNSTIFFENED.LIS')
    #print(*fatiguelist[:2], sep='\n')

    #memcodechecklist = getmemcodecheck('SABSEIS_PRIMARY_ELE_H.LIS')
    #print(*memcodechecklist[:5], sep='\n')
    #print(len(memcodechecklist[3]))

    #list_to_excel(memcodechecklist, 'memcodecheck.xlsx')

    #listsampe = "   hoahoha ohaoh aoho hohaohoha ohoa"
    #parsedline = slices(listsampe, [3, 5 , 3, 5 ])
    #print(parsedline)

    #jointchecklist = getjointcheckiso('SABSEIS_PRIMARYJOINT_ELE_H.LIS')
    #print(jointchecklist[:2])

    apiconelist = getconecheckapi("SABSEIS_CONE_ALE_API.LIS")
    print(apiconelist[:2])