# Proiect BDNSV

## Cuprins

1. [Prezentare și Demo](#prezentare-si-demo)
2. [Rulare Proiect](#rulare-proiect)
3. [Arhitectura Sistemului](#system-architecture)
    - [Data Persistence Layer](#data-persistence-layer)
    - [Application & Logic Layer](#application--logic-layer)
    - [Presentation Layer](#presentation-layer)
4. [Tehnologii Utilizate](#tehnologii-utilizate)
5. [Diagrama Modelului](#diagrame)
6. [Schema Bazei de Date](#schema-bazei-de-date)
    - [Noduri](#1-noduri-node-types)
    - [Relații](#2-relații-relationship-types)
    - [Constrângeri](#3-constrângeri-data-integrity-constraints)
7. [Configurație Software & Hardware](#configurație-software--hardware)
8. [Code Snippets & Execuție](#code-snippets--execuție)
9. [Capturi de Ecran](#capturi-de-ecran)
10. [Analiză Comparativă: Neo4j vs. Oracle SQL](#analiză-comparativă-neo4j-vs-oracle-sql)
11. [Bibliografie](#bibliografie)

---

## Prezentare Si Demo

- Prezentare: [Prezentare](./LinkedIn%20Graph%20Analysis%20%26%20RAG%20Agent.pptx)
- Demo:  [Link către Demo](https://youtu.be/rkJNDs_DHkE)

## Rulare Proiect

**1. Inițializare Date & AI**
Deschideți și rulați comanda **Run All** în următoarele notebook-uri pentru a popula baza de date și a configura agentul:
* [`LinkedInNetwork.ipynb`](./LinkedInNetwork.ipynb) – Schema și populare date.
* [`AgentAI.ipynb`](./AgentAI.ipynb) – Configurare Agent AI.

**2. Lansare Dashboard**
Pentru a porni interfața grafică, rulați comanda:
```bash
streamlit run dashboard.py
```
## System Architecture
- Sistemul este proiectat pe o arhitectură modulară și stratificată, centrată pe o bază de date orientată pe grafuri (Neo4j). Aceasta integrează o interfață de vizualizare interactivă și un agent conversațional bazat pe LLM pentru interogarea datelor.
  ### Data Persistence Layer
  - Tehnologie: Neo4j Graph Database (AuraDB).
  - Rol: Stocarea entităților interconectate (Utilizatori, Companii, Proiecte, Certificări) sub forma unui graf de proprietăți.
  - Structură: Modelul de date este optimizat pentru traversări rapide (Index-Free Adjacency), eliminând necesitatea operațiilor costisitoare de JOIN specifice bazelor relaționale SQL.
  - Initializare: Scripturile de populare și definire a schemei sunt gestionate prin [LinkedInNetwork.ipynb](LinkedInNetwork.ipynb)
  ### Application & Logic Layer
  - Acest strat este implementat în Python 3.12 și gestionează logica de business prin două subsisteme distincte:
    1. Modulul AI & GraphRAG
       - Implementat în AgentAI.ipynb.
       - Utilizează framework-ul LangChain [[6]](https://python.langchain.com/docs/introduction/) pentru a orchestra interacțiunea dintre utilizator și baza de date.
       - LLM Integration: Integrează modelele Google Gemini (via langchain-google-genai) [[7]](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/) pentru a traduce întrebările din limbaj natural în interogări Cypher complexe.
    2. Modulul de Analiză Vizuală
        - Implementat în [dashboard.py](dashboard.py).
        - Gestionează algoritmii de traversare a grafului: Shortest Path, K-hop Neighborhood și Friends-of-Friends.
        - Folosește driverul oficial neo4j pentru execuția directă a interogărilor optimizate.
   ### Presentation Layer
   - Interfață Web: Construită cu Streamlit [[9]](https://docs.streamlit.io/), oferind controale interactive pentru parametrizarea interogărilor
   - Vizualizare Grafică: Utilizează biblioteca PyVis [[10]](https://pyvis.readthedocs.io/en/latest/)( pentru randarea dinamică a sub-grafurilor, permițând utilizatorului să exploreze vizual nodurile și conexiunile returnate de backend.
## Tehnologii Utilizate
- Databases: Neo4j [[1]](https://neo4j.com/docs/), Oracle [[4]](https://docs.oracle.com/en/database/oracle/oracle-database/19/index.html). 
- Backend Language: Python 3.12.
- Frameworks: LangChain, Streamlit.
- AI Models: Google Gemini 1.5 Flash.
- Drivers & Tools: neo4j (Python Driver) [[3]](https://neo4j.com/docs/python-manual/current/), pandas, pyvis.

## Diagrame
<img width="2097" height="1272" alt="BDNSV" src="https://github.com/user-attachments/assets/8fea6caf-b2f4-4a77-a5f4-cb483fc08c67" />

<img width="1761" height="793" alt="bloom-visualisation (2)" src="https://github.com/user-attachments/assets/8968a25e-92cd-477c-ba60-d92d4a4c4f7a" />

## Schema Bazei De Date
### 1. Noduri (Node Types)

| Label | Proprietăți | Descriere |
| :--- | :--- | :--- |
| **User** | `id`, `name`, `role`, `languages`, `soft_skills`, `open_to_work` | Nodul central (Studenți, Angajați, Recruiteri) |
| **Company** | `name`, `industry`, `work_culture`, `city` | Organizații și companii angajatoare |
| **University** | `name`, `country`, `rank` | Instituții de învățământ (pentru rețeaua Alumni) |
| **Project** | `name`, `tech_stack`, `type` | Proiecte (Open Source, Hackathon, Personale) |
| **Certification** | `name`, `issuer`, `difficulty` | Acreditări profesionale (ex: AWS, PMP) |
| **Post** | `id`, `topics`, `timestamp` | Conținut social (articole, știri) pentru interese |

### 2. Relații (Relationship Types)

| Tip Relație | De la -> Către | Proprietăți Cheie | Descriere |
| :--- | :--- | :--- | :--- |
| **WORKS_AT** | `User` -> `Company` | `role`, `current`, `end_year` | Istoricul profesional sau jobul curent |
| **STUDIED_AT** | `User` -> `University` | `degree`, `year` | Conectează userul de Alma Mater |
| **CONTRIBUTED_TO**| `User` -> `Project` | `commits` | Arată implicarea tehnică într-un proiect |
| **EARNED** | `User` -> `Certification`| `year` | Validează competențele userului |
| **FOLLOWS** | `User` -> `User` | *(fără proprietăți)* | Relația socială directă (prietenie/follow) |
| **ENGAGED_WITH** | `User` -> `Post` | `type` (Like, Comment) | Interes implicit (fără follow direct) |

### 3. Constrângeri (Data Integrity Constraints)

| Tip Constrângere | Target (Nod.proprietate) | Descriere                                                                                               |
| :--- | :--- |:--------------------------------------------------------------------------------------------------------|
| **UNIQUENESS** | `User.id` | Asigură că fiecare utilizator are un identificator unic în sistem. |
| **UNIQUENESS** | `Company.name` | Garantează că o companie apare o singură dată în graf (previne duplicate ex: "Google" vs "google").     |
| **UNIQUENESS** | `University.name` | Asigură consistența rețelei de Alumni; toți absolvenții sunt legați de același nod unic.                |
| **UNIQUENESS** | `Post.id` | Identificator unic pentru conținut, necesar pentru a gestiona like-uri și comentarii corect.            |
| **EXISTENCE** | `User.name` | Impune ca orice nod creat cu eticheta `User` să aibă obligatoriu un nume completat.          |

## Configurație Software & Hardware
* **OS:** Windows 11
* **Database Hosting:** Neo4j AuraDB (Cloud)
* **Python Version:** 3.12.
* **Hardware Utilizat:** Procesor Intel/AMD/, 8GB RAM.

## Code Snippets & Execuție

1. Traversare Graf
   - Codul utilizat pentru a găsi cel mai scurt drum între doi utilizatori în [dashboard.py](dashboard.py)
     
   ```python
        MATCH (a:User {{id:$a}}), (b:User {{id:$b}})
        MATCH p = shortestPath((a)-[:FOLLOWS*..{maxlen}]->(b))
        RETURN p
    ```
2. Configurare Agent AI (Python)
    - Inițializarea lanțului GraphCypherQAChain în [AgentAI.ipynb](AgentAI.ipynb):
      
    ```python
        chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=False,
        allow_dangerous_requests=True,
        validate_cypher=True
    )
    ```
## Capturi De Ecran
- Interfața Dashboard
<img width="1826" height="825" alt="Captură de ecran 2026-01-20 155152" src="https://github.com/user-attachments/assets/27f0e9b1-246c-44ba-b628-e4a95d7a91ce" />

- Răspuns Agent AI
<img width="1218" height="640" alt="Captură de ecran 2026-01-20 153543" src="https://github.com/user-attachments/assets/45c391d4-a393-4c6d-b6f9-9699addc031e" />

## Analiză Comparativă: Neo4j vs. Oracle SQL
- Pentru a valida eficiența soluției, am comparat performanța grafului cu o implementare relațională echivalentă (Oracle SQL)

| Scenariu de Testare | Metrica | Oracle SQL (Relațional) | Neo4j (Graf) | Câștigător |
| :--- | :--- | :--- | :--- | :--- |
| **1. Skill-sharing**<br>*(Navigare Locală)* | Timp Execuție | ~1000 ms | **78.52 ms** | **Neo4j** |
| | Complexitate | 6 JOIN-uri | Traversare directă | |
| **2. Mutual Friends**<br>*(Self-Join)* | Timp Execuție | ~1000 ms | **118.82 ms** | **Neo4j** |
| | Mecanism | Nested Loops | Index-Free Adjacency | |
| **3. Stress Test**<br>*(Agregare Masivă)* | Timp Execuție | **3 secunde** | 23 secunde | **SQL** |
| | Volum | ~3 Milioane Rânduri | ~3 Milioane Noduri | |

- Concluzie: Neo4j domină la relații, SQL domină la calcule matematice pe seturi mari.


## Bibliografie
   1. [Neo4j Documentation](https://neo4j.com/docs/)
   2. [Cypher Query Language Reference](https://neo4j.com/docs/cypher-manual/current/)
   3. [Neo4j Python Driver Manual](https://neo4j.com/docs/python-manual/current/)
   4. [Oracle Database 19c Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/index.html)
   5. [Understanding Oracle Execution Plans](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/generating-and-displaying-execution-plans.html)
   6. [LangChain Python Documentation](https://python.langchain.com/docs/introduction/)
   7. [LangChain-Neo4j Cypher Integration](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/)
   8. [Google AI Studio & Gemini API](https://ai.google.dev/docs)
   9. [Streamlit Documentation](https://docs.streamlit.io/)
   10. [PyVis Documentation](https://pyvis.readthedocs.io/en/latest/)
