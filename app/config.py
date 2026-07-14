from	pydantic_settings	import	BaseSettings
class	Settings(BaseSettings):
    database_url:	str
    groq_api_key:	str
    smtp_host:	str
    smtp_port:	int
    smtp_user:	str
    smtp_password:	str
    secret_key:	str
    
class	Config:
    env_file	=	".env"
    settings	=	Settings()