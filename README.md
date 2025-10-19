# Meme-Bong (밈봉) 🚀

<div align="center">

**밈(Meme) 생성 및 공유 플랫폼**

</div>

<br>

## 🖼️ 주요 웹 화면

<table>
  <tr>
    <td align="center"><strong>메인 화면</strong></td>
    <td align="center"><strong>밈 테스트 시연 (GIF)</strong></td>
  </tr>
  <tr>
    <td>
      <img width="1907" height="955" alt="front0" src="https://github.com/user-attachments/assets/5a438fe0-3f05-4d37-9a34-222f9dac4e2e"/>
    </td>
    <td>
    </td>
  </tr>
</table>

| 밈 테스트 페이지                                             |
| :----------------------------------------------------------: |
| <img width="356" alt="image" src="https://github.com/user-attachments/assets/2060f2c6-65cb-4159-9683-70849a00c7ba"/>|
| <img width="2200" alt="front1" src="https://github.com/user-attachments/assets/60437815-4c3e-4a22-b4da-0a04e17b562e" />|

<br>

## 🏗️ 아키텍처 (Architecture)

본 프로젝트는 각 컴포넌트가 Docker 컨테이너로 격리된 서비스 지향 아키텍처를 기반으로 설계되었습니다.

| Component      | Technology   | Role                                                  |
| :------------- | :----------- | :---------------------------------------------------- |
| **Backend** | `FastAPI`    | 비즈니스 로직 처리 및 API 엔드포인트 제공                 |
| **Frontend** | `Nginx`      | 빌드된 정적 웹 애플리케이션 파일을 사용자에게 서빙        |
| **Database** | `PostgreSQL` | 사용자 데이터, 밈 정보 등 정형 데이터 저장 및 관리     |
| **Storage** | `MinIO`      | 이미지, 동영상 등 대용량 객체 파일(비정형 데이터) 저장  |

<br>

## 💻 로컬에서 실행하기

이 프로젝트를 로컬 환경에서 실행하는 방법

#### 1단계: Docker Desktop 실행

가장 먼저, PC에 설치된 Docker Desktop 프로그램을 실행해주세요. 프로그램이 켜지고 고래 아이콘이 안정될 때까지 기다립니다.

#### 2단계: 터미널에서 명령어 실행

터미널을 열고 프로젝트의 최상위 폴더(`meam_bong/`)로 이동한 뒤, 아래의 명령어를 입력하세요.

```bash
docker-compose up --build
````

#### 3단계: 서비스 확인

모든 컨테이너가 성공적으로 실행되었다면, 웹 브라우저에서 아래 주소로 접속하여 각 서비스가 정상 동작하는지 확인합니다.

  - **🖥️ 프론트엔드 (사용자 화면):** [`http://localhost:8080`](https://www.google.com/search?q=http://localhost:8080)
  - **⚙️ 백엔드 API 문서:** [`http://localhost:8000/docs`](https://www.google.com/search?q=http://localhost:8000/docs)
  - **🗄️ MinIO 관리 페이지:** [`http://localhost:9001`](https://www.google.com/search?q=http://localhost:9001)
  - **💾 데이터베이스:** pgAdmin 또는 DBeaver와 같은 툴로 `localhost:5432`에 접속하여 확인

<br>

## 🛠️ 기술 스택

| Category       | Technology                               |
| :------------- | :--------------------------------------- |
| **Frontend** | `Nginx`                                  |
| **Backend** | `Python`, `FastAPI`                      |
| **Database** | `PostgreSQL`                             |
| **Storage** | `MinIO`                                  |
| **DevOps** | `Docker`, `Docker Compose`               |
| **Infra** | `Terraform`, `AWS` (예정)                |

```
```
