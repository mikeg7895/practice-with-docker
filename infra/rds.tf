resource "aws_db_subnet_group" "rds_subnet_gorup" {
  name       = "rds-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "RDS subnet group"
  }
}

resource "aws_db_instance" "rds_postgres" {
  identifier             = "tasks-db"
  engine                 = "postgres"
  engine_version         = "17.4"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  storage_type           = "gp2"
  db_name                = "tasks"
  username               = "postgres"
  password               = "password"
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_gorup.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = false
  multi_az               = false
  apply_immediately      = true
  deletion_protection    = false

  tags = {
    Name = "PostgreSQL"
  }
}