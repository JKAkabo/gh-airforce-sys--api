import uvicorn
from bluestorm.main import app

if __name__ == '__main__':
    uvicorn.run('bluestorm.main:app', reload=True)
