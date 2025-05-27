from fastapi import FastAPI
from datetime import datetime
import pandas as pd
import pytz
from sqlalchemy import create_engine


from fastapi import FastAPI
import uvicorn
from datetime import datetime
import pandas as pd
import pytz
from sqlalchemy import create_engine
import traceback
from fastapi.responses import HTMLResponse

# MySQL 연결 정보
user = "kopo"
password = "kopo"
host = "mysql-container"
port = 3306
database = "timedb"

DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/")
def read_root():

    html_content = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>도형 출력기</title>
    <style>
        body {
            margin: 20px;
            background-color: #E8E8E8
        }
        #input-container {
            width: 400px; /* Set width for the container */
        }
        #txt1 {
            font-size: 1.2rem;
            width: 300px; /* Adjust width to fit placeholder text */
            margin-right: 10px;
        }
        #bt1{
            font-size: 1.2rem;
        }
        #result {
            font-size: 1.5rem;
            width: 400px;
            margin-top: 20px;
            background-color: #ffffff; /* White background */
            border: 1px solid #ccc;
            box-sizing: border-box;

        }
        #result div {
            line-height: 1.2;
        }
    </style>
    </head>
    <body>
        <div id="input-container">
            <input id="txt1" type="text" placeholder="삼각형/역삼각형/피라미드/마름모">
            <input id="bt1" type="button" value="출력">
        </div>
        <div id="result"></div>

        <script>
            const text = document.getElementById("txt1");
            const btn = document.getElementById("bt1");
            const result = document.getElementById("result");

            btn.addEventListener('click', function() {
                const value = text.value.trim();
                result.innerHTML = ""; // 기존 출력 초기화

                if (value === "삼각형") {
                    for (let i = 1; i < 16; i += 2) {
                        const triangleTag = document.createElement("div");
                        let stars = "";
                        for (let j = 0; j < i; j++) {
                            stars += "*";
                        }
                        triangleTag.innerHTML = stars + "<br>";
                        result.append(triangleTag);
                    }

                } else if (value === "역삼각형") {
                    for (let i = 15; i > 0; i -= 2) {
                        const triangleTag = document.createElement("div");
                        let stars = "";
                        for (let j = 0; j < i; j++) {
                            stars += "*";
                        }
                        triangleTag.innerHTML = stars + "<br>";
                        result.append(triangleTag);
                    }
                } else if (value === "피라미드") {
                    for (let i = 1; i <= 15; i += 2) {
                        const pyramidTag = document.createElement("div");
                        let stars = "";
                        for (let j = 0; j < i; j++) {
                            stars += "*";
                        }
                        let spaces = "";
                        for (let k = 0; k < (15 - i) / 2; k++) {
                            spaces += "&nbsp&nbsp;";
                        }
                        pyramidTag.innerHTML = spaces + stars + "<br>";
                        result.append(pyramidTag);
                    }
                } else if (value === "마름모") {
                    // 상단 부분
                    for (let i = 1; i <= 15; i += 2) {
                        const diamondTag = document.createElement("div");
                        let stars = "";
                        for (let j = 0; j < i; j++) {
                            stars += "*";
                        }
                        let spaces = "";
                        for (let k = 0; k < (15 - i) / 2; k++) {
                            spaces += "&nbsp&nbsp";
                        }
                        diamondTag.innerHTML = spaces + stars + "<br>";
                        result.append(diamondTag);
                    }
                    // 하단 부분
                    for (let i = 13; i >= 1; i -= 2) {
                        const diamondTag = document.createElement("div");
                        let stars = "";
                        for (let j = 0; j < i; j++) {
                            stars += "*";
                        }
                        let spaces = "";
                        for (let k = 0; k < (15 - i) / 2; k++) {
                            spaces += "&nbsp&nbsp";
                        }
                        diamondTag.innerHTML = spaces + stars + "<br>";
                        result.append(diamondTag);
                    }
                }
            });
        </script>
    </body>
    </html>
    """

    try:
        now = datetime.now(pytz.timezone('Asia/Seoul'))
        nowType = now.strftime("%Y-%m-%d %H:%M:%S")

        # DB에 저장
        df = pd.DataFrame([{"접속시간": nowType}])
        df.to_sql("userHistory", con=engine, if_exists="append", index=False)

    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())

    return HTMLResponse(content=html_content)



if __name__ == "__main__":
    uvicorn.run("pythondocker:app", host="0.0.0.0", port=9999, log_level="debug",
                proxy_headers=True, reload=True)