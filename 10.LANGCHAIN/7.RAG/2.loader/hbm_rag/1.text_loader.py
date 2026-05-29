from langchain_community.document_loaders import TextLoader

loader = TextLoader('./docs/HBM.txt', encoding='utf-8')
documents = loader.load()

# print(f"불러온 문서 수: {len(documents)}")

doc = documents[0]
print(f"page_content (앞 100자):\n{doc.page_content[:100]}...\n")
print(f"metadata: {doc.metadata}")