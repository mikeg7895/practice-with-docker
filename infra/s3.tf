resource "aws_s3_bucket" "web_site" {
  bucket = "frontend-tasks"
  force_destroy = true # Solo para test

  tags = {
    Name = "Website"
  }
}

resource "aws_s3_bucket_website_configuration" "configuration_website" {
  bucket = aws_s3_bucket.web_site.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_public_access_block" "all-access" {
  bucket = aws_s3_bucket.web_site.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "policy_access_public" {
  bucket = aws_s3_bucket.web_site.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PermitirAccesoPublico",
        Effect    = "Allow",
        Principal = "*",
        Action    = ["s3:GetObject"],
        Resource  = "${aws_s3_bucket.web_site.arn}/*"
      }
    ]
  })
}