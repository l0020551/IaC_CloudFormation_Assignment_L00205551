# Standalone tier directory
* In this directory the three tiers and VPC were developed as standalone stacks for debug.
* RDS is dependent on VPC unless the VPPC was manually gererated
* Applayer.yaml prints database values to console instead of interfacing with the RDS
* App2Db.yaml is the app that does interface with the RDS
* Webpage outputs a broken nginx page. I ran out of time defore it could be debugged but the VPC net and security group for this should work.