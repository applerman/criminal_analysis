import csv
import numpy
from sklearn.feature_extraction import DictVectorizer

def preprocessing(infile, outfile=""):
    with open(infile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        raw_data = dict()
        attr_names = spamreader.next() #['Date, 'Category', ...]
        for attr in attr_names:
            raw_data[attr] = [] # raw_data['Date'] = []
                                # raw_data['Category'] = []
    
        for row in spamreader:
            for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                raw_data[attr_names[i]].append(attr)
                
    
        # Dates -> split into year, month, date, hour (24hr), minute, second (may be all 0)
        raw_data['Year'] = []
        raw_data['Month'] = []
        raw_data['Day'] = []
        raw_data['Hour'] = []
        raw_data['Minute'] = []
        raw_data['Second'] = []
        MONTH = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        for dates in raw_data['Dates']:
            splitted_dates = dates.split(' ')
            ymh = splitted_dates[0].split('-')
            hms = splitted_dates[1].split(':')
            raw_data['Year'].append(int(ymh[0]))
            raw_data['Month'].append(MONTH[int(ymh[1])-1])
            raw_data['Day'].append(int(ymh[2]))
            raw_data['Hour'].append(int(hms[0]))
            raw_data['Minute'].append(int(hms[1]))
            raw_data['Second'].append(int(hms[2]))
    
        dvec = DictVectorizer(sparse=False)
        new_month = dvec.fit_transform(map(lambda x: dict(Month=x), raw_data['Month']))
        for new_attr in dvec.get_feature_names():
            raw_data[new_attr] = []
        for data in new_month:
            for i, val in enumerate(data):
                raw_data[dvec.get_feature_names()[i]].append(val)
    
        # Category -> label them from 0-38
        new_category = dvec.fit_transform(map(lambda x: dict(Category=x), raw_data['Category']))
        for new_attr in dvec.get_feature_names():
            raw_data[new_attr] = []
        for data in new_category:
            for i, val in enumerate(data):
                raw_data[dvec.get_feature_names()[i]].append(val)
        # Descript -> ???
    
        # DayOfWeek -> Convert to 7 binary features (Monday, ..., Sunday)
        new_dayofweek = dvec.fit_transform(map(lambda x: dict(DayOfWeek=x), raw_data['DayOfWeek']))
        for new_attr in dvec.get_feature_names():
            raw_data[new_attr] = []
        for data in new_dayofweek:
            for i, val in enumerate(data):
                raw_data[dvec.get_feature_names()[i]].append(val)
    
        # PdDistrict -> Convert to # binary features
        new_pddistrict = dvec.fit_transform(map(lambda x: dict(PdDistrict=x), raw_data['PdDistrict']))
        for new_attr in dvec.get_feature_names():
            raw_data[new_attr] = []
        for data in new_pddistrict:
            for i, val in enumerate(data):
                raw_data[dvec.get_feature_names()[i]].append(val)
    
        # Resolution -> ???
    
        # Address -> ???
    
        # X -> will use raw data, as well as features incorporated from SF OpenData
        raw_data['X'] = map(float, raw_data['X'])
    
        # Y -> same as above
        raw_data['Y'] = map(float, raw_data['Y'])
    
        if outfile:
            with open(outfile, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(raw_data.keys())
                for row in zip(*list(raw_data.values())):
                    writer.writerow(row)
            
def main():
    preprocessing('train.csv', 'new_train.csv')

if __name__ == "__main__":
    # execute only if run as a script
    main()
