import pulumi
from pulumi_aws import s3, cloudfront

# Create S3 bucket for static website
bucket = s3.Bucket(
    "static-website-bucket",
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
        error_document="error.html"
    ),
    acl="public-read"
)

# Upload sample HTML files
index_content = """
<html><body><h1>Welcome to Girisha Pulumi Lab 7!</h1></body></html>
"""
error_content = """
<html><body><h1>Error Page</h1></body></html>
"""

s3.BucketObject(
    "index.html",
    bucket=bucket.id,
    content=index_content,
    content_type="text/html",
    acl="public-read"
)

s3.BucketObject(
    "error.html",
    bucket=bucket.id,
    content=error_content,
    content_type="text/html",
    acl="public-read"
)

# Create CloudFront distribution
distribution = cloudfront.Distribution(
    "static-distribution",
    enabled=True,
    default_root_object="index.html",
    origins=[cloudfront.DistributionOriginArgs(
        domain_name=bucket.bucket_regional_domain_name,
        origin_id=bucket.id,
        s3_origin_config=cloudfront.DistributionOriginS3OriginConfigArgs(
            origin_access_identity="origin-access-identity/cloudfront/static-website"
        )
    )],
    default_cache_behavior=cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=["GET", "HEAD"],
        cached_methods=["GET", "HEAD"],
        target_origin_id=bucket.id,
        viewer_protocol_policy="redirect-to-https",
        forwarded_values=cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=False,
            cookies=cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                forward="none"
            )
        )
    ),
    restrictions=cloudfront.DistributionRestrictionsArgs(
        geo_restriction=cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none"
        )
    ),
    viewer_certificate=cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True
    )
)

# Export outputs
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_endpoint", bucket.website_endpoint)
pulumi.export("cloudfront_url", distribution.domain_name)