from modules.aws import aws
import json
import sys

def get_resouces(account_id, region):
    session = aws(account_id,region)
    
    result = []
    result.extend(session.get_ec2_instances())
    result.extend(session.get_rds_instances())
    result.extend(session.get_elasticache_redis_instances())
    result.extend(session.get_elasticache_memcached_instances())
    result.extend(session.get_ecs_fargate_clusters())
    result.extend(session.get_cloudfront_destributions())
    result.extend(session.get_dynamodb_tables())
    result.extend(session.get_redshift_instances())
    result.extend(session.get_lambda_functions())
    
    return result

if __name__ == '__main__':
    account_id = sys.argv[1]

    result = []
    with open('regions.txt', 'r', newline='') as f:
        for region in f:
            result.extend(get_resouces(account_id,region.rstrip('\n')))
    
    # output
    with open( account_id + '_output.txt', 'w') as fo:
        for r in result:
            fo.write(json.dumps(r) + '\n')
        