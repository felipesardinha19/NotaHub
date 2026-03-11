# 📚 NotaHub

Aplicação para estudantes que permite **controlar faltas por carga horária** e acompanhar o risco de reprovação em disciplinas.

O sistema calcula automaticamente a **frequência do aluno** com base nas horas de aula registradas.

---

## 🎯 Problema

Muitos estudantes têm dificuldade em acompanhar quantas faltas ainda podem ter antes de reprovar por frequência.

O **NotaHub** resolve isso calculando automaticamente:

- frequência atual
- horas faltadas
- horas restantes
- risco de reprovação

---

## ⚙️ Tecnologias

- 🐍 Python
- 🎨 Streamlit
- 🗄️ SQLite
- 📊 Pandas

---

## 🧠 Regras de Negócio

Com base em uma pesquisa que fiz com estudantes da USP de Ribeirão Preto, a presença mínima exigida geralmente é:

- **70% de presença**
- **30% máximo de faltas**

O NotaHub utiliza essas regras para calcular automaticamente a situação do aluno.

### Exemplo

Disciplina com **60 horas totais**

- Máximo de faltas: **15 horas**
- Presença mínima: **45 horas**

O sistema acompanha automaticamente esses valores.

---

## 🔄 Funcionamento

Fluxo do sistema:

Cadastro da disciplina  
⬇️  
Definição da carga horária total  
⬇️  
Registro das aulas (data e duração)  
⬇️  
Registro de presença ou falta  
⬇️  
Cálculo automático da frequência  

---

## 📊 Dashboard

O sistema mostra para cada disciplina:

- 📈 Frequência atual
- ⏳ Horas restantes
- ❌ Horas faltadas
- ⚠️ Status de risco

Status possíveis:

- 🟢 **OK**
- 🟡 **Risco**
- 🔴 **Reprovado**
