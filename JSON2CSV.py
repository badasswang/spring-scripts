import sys
import json
import csv

reload(sys)
sys.setdefaultencoding('utf8')

def reduce_item(key, value):
    global reduced_item
    
    
    if type(value) is list:
        i=0
        for sub_item in value:
            if type(sub_item) is dict:
                sub_sub_keys = sub_item.keys()
                for sub_sub_key, sub_sub_item in sub_item.items():
                    reduce_item(key+'_'+str(sub_sub_key), sub_item[sub_sub_key]) 
            else:
                reduce_item(key+'_'+str(i), sub_item)
            i=i+1

    
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key+'_'+str(sub_key), value[sub_key])
    
    else:
        reduced_item[str(key)] = str(value)

if __name__ == "__main__":
        node = sys.argv[1]
        json_file_path = sys.argv[2]
        csv_file_path = sys.argv[3]

        fp = open(sys.argv[2], 'r')
        json_value = fp.read()
        raw_data = json.loads(json_value)

        processed_data = []
        header = []
        for item in raw_data[node]:
            reduced_item = {}
            reduce_item(node, item)

            header += reduced_item.keys()

            processed_data.append(reduced_item)

        header = list(set(header))
        header.sort()

        with open(sys.argv[3], 'wb+') as f:
            writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)

        print "CSV file with %d coloumns completed." % len(header)
