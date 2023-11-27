import boto3

## 出力フォーマット
### account_id: AWSアカウントID
### service: サービス名
### region: リージョン名
### id: リソース識別子
### type: リソースタイプ

class aws:
    def __init__(self, account_id, region_name):
        try:
            self.account_id = account_id
            self.region_name = region_name
            self.session = boto3.Session(
#                profile_name=profile_name
                region_name=region_name
                )
        except Exception as e:
            exit('ERROR: Profile not found : {}'.format(e))

    def get_ec2_instances(self):
        try:
            ec2list = self.session.resource('ec2').instances.all()
        except Exception as e:
            exit('ERROR: Could not get instances : {}'.format(e))
        else:
            result = []
            for e in ec2list:
                result.append({
                    'account_id': self.account_id,
                    'service': 'ec2',
                    'region':   self.region_name,
                    'id': e.id,
                    'type': e.instance_type,
#                    'state': e.state['Name'],
#                    'public_ip': e.public_ip_address,
#                    'private_ip': e.private_ip_address,
#                    'tags': e.tags
                    })
            print(result)
            return result

    def get_rds_instances(self):
        try:
            rdslist = self.session.client('rds').describe_db_instances()
        except Exception as e:
            exit('ERROR: Could not get instances : {}'.format(e))
        else:
            result = []
            for r in rdslist['DBInstances']:
                result.append({
                    'account_id': self.account_id,
                    'service': 'rds',
                    'region':   self.region_name,
                    'id': r['DBInstanceIdentifier'],
                    'type': r['DBInstanceClass'],
#                    'state': r['DBInstanceStatus'],
#                    'public_ip': r['Endpoint']['Address'],
#                    'private_ip': r['Endpoint']['Address'],
                    })
            print(result)
            return result
    
    def get_elasticache_redis_instances(self):
        try:
            elasticachelist = self.session.client('elasticache').describe_cache_clusters()
        except Exception as e:
            exit('ERROR: Could not get instances : {}'.format(e))
        else:
            result = []
            for e in elasticachelist['CacheClusters']:
                if e['Engine'] == 'redis':
                    result.append({
                        'account_id': self.account_id,
                        'service': 'elasticache_redis',
                        'region':   self.region_name,
                        'id': e['CacheClusterId'],
                        'type': e['CacheNodeType'],
#                        'state': e['CacheClusterStatus'],
#                        'public_ip': e['ConfigurationEndpoint']['Address'],
#                        'private_ip': e['ConfigurationEndpoint']['Address'],
                        })
            print(result)
            return result
    
    def get_elasticache_memcached_instances(self):
        try:
            elasticachelist = self.session.client('elasticache').describe_cache_clusters()
        except Exception as e:
            exit('ERROR: Could not get instances : {}'.format(e))
        else:
            result = []
            for e in elasticachelist['CacheClusters']:
                if e['Engine'] == 'memcached':
                    result.append({
                        'account_id': self.account_id,
                        'service': 'elasticache_memcached',
                        'region':   self.region_name,
                        'id': e['CacheClusterId'],
                        'type': e['CacheNodeType'],
#                        'state': e['CacheClusterStatus'],
#                        'public_ip': e['ConfigurationEndpoint']['Address'],
#                        'private_ip': e['ConfigurationEndpoint']['Address'],
                        })
            print(result)
            return result
        
    def get_dynamodb_tables(self):
        try:
            dynamodblist = self.session.client('dynamodb').list_tables()
        except Exception as e:
            exit('ERROR: Could not get tables : {}'.format(e))
        else:
            result = []
            for d in dynamodblist['TableNames']:
                result.append({
                    'account_id': self.account_id,
                    'service': 'dynamodb',
                    'region':   self.region_name,
                    'id': d,
                    'type': '',
#                    'state': 'active',
                    })
            print(result)
            return result
    
    def get_cloudfront_destributions(self):
        if self.region_name != 'us-west-1':
            return []
        else:
            try:
                cloudfrontlist = self.session.client('cloudfront').list_distributions()
            except Exception as e:
                exit('ERROR: Could not get distributions : {}'.format(e))
            else:
                result = []
                if 'Items' in cloudfrontlist['DistributionList']:
                    for c in cloudfrontlist['DistributionList']['Items']:
                        result.append({
                            'account_id': self.account_id,
                            'service': 'cloudfront',
                            'region':   self.region_name,
                            'id': c['Id'],
                            'type': '',
                            #'state': c['Status'],
                            #'tags': []
                            })
                print(result)
                return result
        
    def get_opensearch_instances(self):
        try:
            opensearchlist = self.session.client('opensearch').list_domain_names()
        except Exception as e:
            exit('ERROR: Could not get instances : {}'.format(e))
        else:
            result = []
            for o in opensearchlist['DomainNames']:
                result.append({
                    'account_id': self.account_id,
                    'service': 'opensearch',
                    'region':   self.region_name,
                    'id': o['DomainName'],
                    'type': o['EngineType'],
                    #'state': o['DomainStatus']['State'],
                    #'tags': []
                    })
            print(result)
            return result
    
    def get_redshift_instances(self):
        try:
            redshiftlist = self.session.client('redshift').describe_clusters()
        except Exception as e:
            exit('ERROR: Could not get instances : {}'.format(e))
        else:
            result = []
            for r in redshiftlist['Clusters']:
                result.append({
                    'account_id': self.account_id,
                    'service': 'redshift',
                    'region':   self.region_name,
                    'id': r['ClusterIdentifier'],
                    'type': r['NodeType'],
                    })
            print(result)
            return result
    
    def get_ecs_fargate_clusters(self):
        try:
            ecslist = self.session.client('ecs').list_clusters()
        except Exception as e:
            exit('ERROR: Could not get clusters : {}'.format(e))
        else:
            result = []
            for e in ecslist['clusterArns']:
                result.append({
                    'account_id': self.account_id,
                    'service': 'ecs_fargate',
                    'region':   self.region_name,
                    'id': e.split('/')[1],
                    'type': '',
                    })
            print(result)
            return result
        
    def get_lambda_functions(self):
        try:
            lambdalist = self.session.client('lambda').list_functions()
        except Exception as e:
            exit('ERROR: Could not get functions : {}'.format(e))
        else:
            result = []
            for l in lambdalist['Functions']:
                result.append({
                    'account_id': self.account_id,
                    'service': 'lambda',
                    'region':   self.region_name,
                    'id': l['FunctionName'],
                    'type': 'lambda',
                    })
            print(result)
            return result
    
    