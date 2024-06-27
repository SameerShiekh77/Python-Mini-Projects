import requests
import csv

# Define the CSV file and headers
csv_file = 'new_contract_awards_list.csv'
csv_headers = [
    'Contract Award Date', 'Contract Award Number', 'CAGE CODE',
    'Contractor Unique Entity ID', 'Contractor Awarded Name', 'Total Contract Value', 'Contractor Awarded Email', 'full_name','Posted by '
]
print("Script has been started")
# Create and open the CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)  # Write the headers to the CSV file

    for page in range(56273):
        print('page no: ', page)
        url = f'https://sam.gov/api/prod/sgs/v1/search/?random=1718563700978&index=opp&page={page}&sort=-modifiedDate&size=100&mode=search&responseType=json&q=&qMode=ALL&notice_type=a'
        
        r = requests.get(url)
        data = r.json()
        for index in range(100):
            try:
                id = data['_embedded']['results'][index]['_id']
                print(id)
                
                award_detail_url = f'https://sam.gov/api/prod/opps/v2/opportunities/{id}?random=1718565025250'
                award_detail_data = requests.get(award_detail_url)
                
                try:
                    award_detail_data = award_detail_data.json()
                    award_data = award_detail_data['data2']['award']
                    contract_award_date = award_data['date']
                    contract_award_number = award_data['number']
                    try:
                        cageCode = award_data['awardee']['cageCode']
                    except Exception as e:
                        print("cageCode is not found due to:" ,e)
                        cageCode = "Not Found"
                        
                    try:
                        unique_id = award_data['awardee']['ueiSAM']
                    except Exception as e:
                        print("Unique id is not found: ", unique_id)
                        unique_id = "Not Found"
                    
                    
                    try:
                        award_name = award_data['awardee']['name']
                    except Exception as e:
                        print("award name is not found: ", award_name)
                        award_name = "Not Found"
                        
                    contract_amount = award_data['amount']
                    
                    
                    try:
                        email = award_detail_data['data2']['pointOfContact'][0]['email']
                        full_name = award_detail_data['data2']['pointOfContact'][0]['fullName']
                    except Exception as e:
                        print("Point of Contact not found ",e)
                        email = "Not Found"
                        full_name = 'Not Found'
                    
                    # Write the data to the CSV file
                    writer.writerow([
                        contract_award_date, contract_award_number, cageCode,
                        unique_id, award_name, contract_amount, email, full_name,'Sameer'
                    ])
                    
                except Exception as e:
                    print('id error: ', e)
                    print(index)
                
            except Exception as e:
                print("page error: ", e)
                print("page: ",page)

print("Script has been completed")