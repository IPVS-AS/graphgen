cat "2022-03-11 19:28:16.409035-A Planning-92ad4548-c756-45ac-89bd-f99b1df23058.gz" \
| gsed -r 's|";|"	[minlen=1,lblstyle="flow"];|g' \
| gsed -r 's|\[minlen=1\];|[minlen=1,lblstyle="flow"];|g' \
| gsed -r 's|label="D([^"]+)"\];|label="D\1",lblstyle="dataset_s"\];|g' \
| gsed -r 's|label="A([^"]+)"\];|label="A\1",lblstyle="activity"\];|g' \
| gsed -r 's|label="A Planning ([^"]+)|label="P_{\1}|g' \
| gsed -r 's|label="A Testing ([^"]+)|label="T_{\1}|g' \
| gsed -r 's|label="A Simulation ([^"]+)|label="S_{\1}|g' \
| gsed -r 's|label="A Construction ([^"]+)|label="C_{\1}|g' \
| gsed -r 's|label="D Planning ([^"]+)|label="D_{P_{\1}}|g' \
| gsed -r 's|label="D Testing ([^"]+)|label="D_{T_{\1}}|g' \
| gsed -r 's|label="D Simulation ([^"]+)|label="D_{S_{\1}}|g' \
| gsed -r 's|label="D Construction ([^"]+)|label="D_{C_{\1}}|g' > g1.dot

cat "2022-03-11 19:35:11.329883-A Planning-31219b38-6683-4f38-98ee-7e3324fc4789.gz" \
| gsed -r 's|";|"	[minlen=1,lblstyle="flow"];|g' \
| gsed -r 's|\[minlen=1\];|[minlen=1,lblstyle="flow"];|g' \
| gsed -r 's|label="D([^"]+)"\];|label="D\1",lblstyle="dataset_s"\];|g' \
| gsed -r 's|label="A([^"]+)"\];|label="A\1",lblstyle="activity"\];|g' \
| gsed -r 's|label="A Planning ([^"]+)|label="P_{\1}|g' \
| gsed -r 's|label="A Testing ([^"]+)|label="T_{\1}|g' \
| gsed -r 's|label="A Simulation ([^"]+)|label="S_{\1}|g' \
| gsed -r 's|label="A Construction ([^"]+)|label="C_{\1}|g' \
| gsed -r 's|label="D Planning ([^"]+)|label="D_{P_{\1}}|g' \
| gsed -r 's|label="D Testing ([^"]+)|label="D_{T_{\1}}|g' \
| gsed -r 's|label="D Simulation ([^"]+)|label="D_{S_{\1}}|g' \
| gsed -r 's|label="D Construction ([^"]+)|label="D_{C_{\1}}|g' > g2.dot

dot2tex --autosize -ftikz -tmath g1.dot > g1.tex
dot2tex --autosize -ftikz -tmath g2.dot > g2.tex