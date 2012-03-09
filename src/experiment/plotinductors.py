import csv



inductorReader = csv.DictReader(open('Y:\Python\emcworkbench\data\inductance_dump.csv','rb'))

coolInductors = []
for inductor in inductorReader:
    try:
        float(inductor['q_factor'])
    except:
        pass
#         print('Threw away %s',inductor['mpn'])
    else:
        try:
            float(inductor['resonant_frequency'])
        except:
            pass
        else:
            coolInductors.append(inductor)

print numel(coolInductors)

