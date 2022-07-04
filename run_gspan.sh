#!/bin/bash



mkdir -p output

python3 -mgspan_mining "--min_support=100" "--directed=true" "./graphs/graphs-combined-err-0.0-gspan" > "./output/graphs-combined-err-0.0-gspan-supp-100"
python3 -mgspan_mining "--min_support=90" "--directed=true" "./graphs/graphs-combined-err-0.0-gspan" > "./output/graphs-combined-err-0.0-gspan-supp-90"
python3 -mgspan_mining "--min_support=80" "--directed=true" "./graphs/graphs-combined-err-0.0-gspan" > "./output/graphs-combined-err-0.0-gspan-supp-80"
python3 -mgspan_mining "--min_support=70" "--directed=true" "./graphs/graphs-combined-err-0.0-gspan" > "./output/graphs-combined-err-0.0-gspan-supp-70"
python3 -mgspan_mining "--min_support=60" "--directed=true" "./graphs/graphs-combined-err-0.0-gspan" > "./output/graphs-combined-err-0.0-gspan-supp-60"
python3 -mgspan_mining "--min_support=50" "--directed=true" "./graphs/graphs-combined-err-0.0-gspan" > "./output/graphs-combined-err-0.0-gspan-supp-50"

python3 -mgspan_mining "--min_support=100" "--directed=true" "./graphs/graphs-combined-err-0.01-gspan" > "./output/graphs-combined-err-0.01-gspan-supp-100"
python3 -mgspan_mining "--min_support=90" "--directed=true" "./graphs/graphs-combined-err-0.01-gspan" > "./output/graphs-combined-err-0.01-gspan-supp-90"
python3 -mgspan_mining "--min_support=80" "--directed=true" "./graphs/graphs-combined-err-0.01-gspan" > "./output/graphs-combined-err-0.01-gspan-supp-80"
python3 -mgspan_mining "--min_support=70" "--directed=true" "./graphs/graphs-combined-err-0.01-gspan" > "./output/graphs-combined-err-0.01-gspan-supp-70"
python3 -mgspan_mining "--min_support=60" "--directed=true" "./graphs/graphs-combined-err-0.01-gspan" > "./output/graphs-combined-err-0.01-gspan-supp-60"
python3 -mgspan_mining "--min_support=50" "--directed=true" "./graphs/graphs-combined-err-0.01-gspan" > "./output/graphs-combined-err-0.01-gspan-supp-50"

python3 -mgspan_mining "--min_support=100" "--directed=true" "./graphs/graphs-combined-err-0.04-gspan" > "./output/graphs-combined-err-0.04-gspan-supp-100"
python3 -mgspan_mining "--min_support=90" "--directed=true" "./graphs/graphs-combined-err-0.04-gspan" > "./output/graphs-combined-err-0.04-gspan-supp-90"
python3 -mgspan_mining "--min_support=80" "--directed=true" "./graphs/graphs-combined-err-0.04-gspan" > "./output/graphs-combined-err-0.04-gspan-supp-80"
python3 -mgspan_mining "--min_support=70" "--directed=true" "./graphs/graphs-combined-err-0.04-gspan" > "./output/graphs-combined-err-0.04-gspan-supp-70"
python3 -mgspan_mining "--min_support=60" "--directed=true" "./graphs/graphs-combined-err-0.04-gspan" > "./output/graphs-combined-err-0.04-gspan-supp-60"
python3 -mgspan_mining "--min_support=50" "--directed=true" "./graphs/graphs-combined-err-0.04-gspan" > "./output/graphs-combined-err-0.04-gspan-supp-50"

python3 -mgspan_mining "--min_support=100" "--directed=true" "./graphs/graphs-combined-err-0.05-gspan" > "./output/graphs-combined-err-0.05-gspan-supp-100"
python3 -mgspan_mining "--min_support=90" "--directed=true" "./graphs/graphs-combined-err-0.05-gspan" > "./output/graphs-combined-err-0.05-gspan-supp-90"
python3 -mgspan_mining "--min_support=80" "--directed=true" "./graphs/graphs-combined-err-0.05-gspan" > "./output/graphs-combined-err-0.05-gspan-supp-80"
python3 -mgspan_mining "--min_support=70" "--directed=true" "./graphs/graphs-combined-err-0.05-gspan" > "./output/graphs-combined-err-0.05-gspan-supp-70"
python3 -mgspan_mining "--min_support=60" "--directed=true" "./graphs/graphs-combined-err-0.05-gspan" > "./output/graphs-combined-err-0.05-gspan-supp-60"
python3 -mgspan_mining "--min_support=50" "--directed=true" "./graphs/graphs-combined-err-0.05-gspan" > "./output/graphs-combined-err-0.05-gspan-supp-50"
