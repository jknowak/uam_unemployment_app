## Bezrobocie w Polsce, przed i w trakcie pandemii COVID-19

Jest to aplikacja napisana w Dashu na zaliczenie zajęć na Uniwersytecie Adama Mickiewicza prowadzonych przez @psobczyk.

### Jak uruchomić aplikację?

```bash
python3 src/app.py
```

i odwiedź http://127.0.0.1:8050/ w przeglądarce.

### Budowanie i uruchamianie aplikacji w Dockerze

```bash
docker build -t uam-dash .

docker run --rm -p 8000:8000 uam-dash
```


### How to contribute

Before commiting make sure that your code passes black and pylint checks.
