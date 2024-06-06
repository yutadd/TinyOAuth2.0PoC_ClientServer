class User:
    id:int
    token:str
    token_type:str
    expires_at:str
    refresh_token:str
    scope:str
    session_id:str
    def __init__(self,id:int,token:str,token_type:str,expires_at:str,refresh_token:str,scope:str,session_id:str) -> None:
        self.id=id
        self.token=token
        self.token_type=token_type
        self.expires_at=expires_at
        self.refresh_token=refresh_token
        self.scope=scope
        self.session_id=session_id