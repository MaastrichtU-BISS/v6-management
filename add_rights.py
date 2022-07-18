from vantage6.client import Client

client = Client("path_to_rest_service", 443, "/api")
client.authenticate("root", "")
client.setup_encryption(None)

# Specify roles for org admins
all_rules = client.rule.list()
for rule in all_rules:
    print(f'{rule["id"]} | {rule["operation"]} | {rule["name"]} | {rule["scope"]}')

# Can do anything at ORGANIZATION level
rules = [rule['id'] for rule in all_rules if rule['scope'] == 'ORGANIZATION']
# But also manage tasks within collaboration (without deletion)
rules.extend([rule['id'] for rule in all_rules if rule['scope'] == 'GLOBAL' 
                and rule['name'] == 'task'
                and rule['operation'] != 'DELETE'])

# Remove some rules
rules = [
    rule for rule in rules if rule not in [
        8, # Delete node
    ]
]

# Find client based on username
clientName = 'university-of-leeds'
clientId = None
for user in client.user.list():
    print(f"{user['id']} | {user['username']}")

    if clientName in str(user['username']):
        print("found")
        clientId = user['id']
        break

## update rules for found user ID
client.user.update(id_ = clientId, rules=rules)

## Check if rules have been applied
targetClient = client.user.get(clientId)
for foundRule in targetClient.get('rules'):
    print(foundRule['id'])