# Proiect BDNSV
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
       - Utilizează framework-ul LangChain pentru a orchestra interacțiunea dintre utilizator și baza de date.
       - LLM Integration: Integrează modelele Google Gemini (via langchain-google-genai) pentru a traduce întrebările din limbaj natural în interogări Cypher complexe.
    2. Modulul de Analiză Vizuală
        - Implementat în [dashboard.py](dashboard.py).
        - Gestionează algoritmii de traversare a grafului: Shortest Path, K-hop Neighborhood și Friends-of-Friends.
        - Folosește driverul oficial neo4j pentru execuția directă a interogărilor optimizate.
   ### Presentation Layer
   - Interfață Web: Construită cu Streamlit, oferind controale interactive pentru parametrizarea interogărilor
   - Vizualizare Grafică: Utilizează biblioteca PyVis pentru randarea dinamică a sub-grafurilor, permițând utilizatorului să exploreze vizual nodurile și conexiunile returnate de backend.
## Tehnologii Utilizate
- Databases: Neo4j, Oracle.
- Backend Language: Python 3.12.
- Frameworks: LangChain, Streamlit.
- AI Models: Google Gemini 2.0 Flash.
- Drivers & Tools: neo4j (Python Driver), pandas, pyvis.

## Diagrama

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

##Capturi De Ecran

## Bibliografie
1. Baze de Date & Limbaje de Interogare
   - [Neo4j Documentation](https://neo4j.com/docs/)
   - [Cypher Query Language Reference](https://neo4j.com/docs/cypher-manual/current/)
   - [Neo4j Python Driver Manual](https://neo4j.com/docs/python-manual/current/)
   - [Oracle Database 19c Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/index.html)
   - [Understanding Oracle Execution Plans](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/generating-and-displaying-execution-plans.html)
2. AI & Frameworks
   - [LangChain Python Documentation](https://python.langchain.com/docs/introduction/)
   - [LangChain-Neo4j Cypher Integration](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/)
   - [Google AI Studio & Gemini API](https://ai.google.dev/docs)

3. Interfață & Vizualizare
   - [Streamlit Documentation](https://docs.streamlit.io/)
   - [PyVis Documentation](https://pyvis.readthedocs.io/en/latest/)
