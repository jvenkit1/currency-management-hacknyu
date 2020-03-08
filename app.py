import os
from src.app import create

app=create()

if __name__=="__main__":
    # PORT = os.getenv('PORT')
    PORT=3000
    app.run(host='0.0.0.0', port=PORT, debug=True)
