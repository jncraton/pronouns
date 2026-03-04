import json
import re
import sys
import urllib.request
import urllib.parse
import time
import ssl

def get_wikidata_id(name):
    query = f'https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&search={urllib.parse.quote(name)}&limit=1&origin=*'
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(query, headers={'User-Agent': 'PronounApp/1.0 (https://example.com/)'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            if data.get('search'):
                return data['search'][0]['id']
    except Exception as e:
        print(f"Error fetching {name}: {e}", file=sys.stderr)
    return None

def update_html():
    with open('index.html', 'r') as f:
        content = f.read()

    male_names = [
        'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles',
        'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua',
        'Kenneth', 'Kevin', 'Brian', 'George', 'Timothy', 'Ronald', 'Edward', 'Jason', 'Jeffrey', 'Gary',
        'Ryan', 'Nicholas', 'Eric', 'Stephen', 'Jacob', 'Larry', 'Jonathan', 'Scott', 'Raymond', 'Justin',
        'Brandon', 'Gregory', 'Samuel', 'Benjamin', 'Patrick', 'Jack', 'Alexander', 'Dennis', 'Jerry', 'Tyler',
        'Aaron', 'Henry', 'Douglas', 'Peter', 'Jose', 'Adam', 'Zachary', 'Walter', 'Nathan', 'Harold',
        'Kyle', 'Carl', 'Arthur', 'Gerald', 'Roger', 'Keith', 'Jeremy', 'Terry', 'Lawrence', 'Sean',
        'Christian', 'Albert', 'Joe', 'Ethan', 'Austin', 'Jesse', 'Willie', 'Billy', 'Bryan', 'Bruce',
        'Jordan', 'Ralph', 'Eugene', 'Wayne', 'Louis', 'Dylan', 'Alan', 'Juan', 'Noah', 'Russell', 'Harry',
        'Randy', 'Philip', 'Vincent', 'Gabriel', 'Bobby', 'Johnny'
    ]

    female_names = [
        'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen',
        'Lisa', 'Nancy', 'Betty', 'Sandra', 'Margaret', 'Ashley', 'Kimberly', 'Emily', 'Donna', 'Michelle',
        'Dorothy', 'Carol', 'Amanda', 'Melissa', 'Deborah', 'Stephanie', 'Rebecca', 'Sharon', 'Laura', 'Cynthia',
        'Kathleen', 'Amy', 'Shirley', 'Angela', 'Helen', 'Anna', 'Brenda', 'Pamela', 'Nicole', 'Emma',
        'Samantha', 'Katherine', 'Christine', 'Debra', 'Rachel', 'Catherine', 'Carolyn', 'Janet', 'Ruth', 'Maria',
        'Heather', 'Diane', 'Virginia', 'Julie', 'Joyce', 'Victoria', 'Olivia', 'Kelly', 'Christina', 'Lauren',
        'Joan', 'Evelyn', 'Judith', 'Megan', 'Cheryl', 'Andrea', 'Hannah', 'Martha', 'Jacqueline', 'Frances',
        'Gloria', 'Ann', 'Teresa', 'Kathryn', 'Sara', 'Janice', 'Jean', 'Alice', 'Madison', 'Doris',
        'Abigail', 'Julia', 'Judy', 'Grace', 'Denise', 'Amber', 'Marilyn', 'Beverly', 'Danielle', 'Theresa',
        'Sophia', 'Marie', 'Diana', 'Brittany', 'Natalie', 'Isabella', 'Charlotte', 'Rose', 'Alexis', 'Kayla'
    ]

    male_map = {}
    for name in male_names:
        qid = get_wikidata_id(name)
        if qid:
            male_map[name] = qid
        time.sleep(0.1)

    female_map = {}
    for name in female_names:
        qid = get_wikidata_id(name)
        if qid:
            female_map[name] = qid
        time.sleep(0.1)

    def format_map(m, label):
        entries = []
        items = list(m.items())
        for i in range(0, len(items), 10):
            chunk = items[i:i+10]
            line = ", ".join([f"'{k}': '{v}'" for k, v in chunk])
            entries.append(f"        {line},")
        return f"      const {label} = {{\n" + "\n".join(entries) + "\n      }"

    male_str = format_map(male_map, "PRECACHED_MALE")
    female_str = format_map(female_map, "PRECACHED_FEMALE")

    content = re.sub(r'const PRECACHED_MALE = \{.*?\}' , male_str, content, flags=re.DOTALL)
    content = re.sub(r'const PRECACHED_FEMALE = \{.*?\}', female_str, content, flags=re.DOTALL)

    with open('index.html', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    update_html()
