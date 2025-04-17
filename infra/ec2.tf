resource "aws_instance" "tasks" {
  ami                         = "ami-0ec6efc9adeeaf0ac"
  instance_type               = "t2.micro"
  subnet_id                   = module.vpc.public_subnets[0]
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  key_name                    = "clave"
  associate_public_ip_address = true


  tags = {
    Name = "Tasks web"
  }
}


