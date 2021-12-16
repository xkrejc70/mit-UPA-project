# mit-UPA-project


UPA - Data Storage and Preparation - Project, the 1st Part: Data Processing and Storage Design, Project, the 2nd Part: Extraction, Storage, and Data Processing System Implementation

# Task

== Zadání 1. části ==

Seznamte se s nabízenými tématy pro řešení projektů, které popisují zdroje dat (odkazy na datové sady) a dotazy, které je potřeba na základě těchto dat zodpovědět.

Zvolte si jeden z nabízených zdrojů dat (téma projektu) a analyzujte dílčí datové sady z daného zdroje, jejich strukturu (schéma), typy datových položek, identifikátory, možnosti propojení datových sad (společné entity) či napojení na externí data (jiné zdroje, entity reálného světa, např. polohu v geografickém prostoru), změnu dat v čase (temporální data), a jiné. Po dohodě se cvičícími je zde v některých případech možné zvolit vlastní zdroj dat.

Navrhněte vhodný způsob načtení datových sad z daného zdroje a jejich uložení ve zvolené NoSQL databázi (s výběrem vhodné NoSQL databáze Vám pomohou cvičení z předmětu; jedná se často pro nestrukturovaná či velká data).

Implementujte systém pro získávání, předzpracování, uložení dat do/ve zvolené NoSQL databázi

Výsledné řešení 1. části odevzdejte do WISu. Očekává se, že odevzdáte nejen dokumentaci z analýzy datových sad a z návrhu řešení pro načtení a uložení v NoSQL, ale také zdrojové kódy řešení (skripty, aplikace, schémata, atp.) a stručnou dokumentaci jeho zprovoznění, případně také příklady zajímavých problémů, se kterými jste se v průběhu řešení setkali. Dokumentaci (mimo zdrojové kódy) odevzdávejte ve formátu PDF či jako prostý text v kódování ASCII/UTF-8.

== Zadání 2.části ==

Zvolte si dva úkoly/dotazy ze skupiny A a jeden úkol/dotaz ze skupiny B k řešenému tématu. 

Vymyslete dva vlastní nové úkoly/dotazy, neuvedené u tématu. Jeden z úkolů/dotazů musí vyžadovat kombinaci dat alespoň ze dvou zdrojů. 

Pro všechny zvolené dotazy implementujte nástroj pro extrakci potřebných dat z původního úložiště vytvořeného v první části projektu do souboru/souborů v CSV formátu.

Pro všechny zvolené dotazy navrhněte a implementujte řešení, které tyto dotazy zodpoví. Toto řešení bude již pracovat s daty ve formátu CSV. 

Všechny zvolené dotazy a získané výsledky prezentujte v jednoduché dokumentaci nebo prezentaci.

Zvolte si jednu z dolovacích úloh ze skupiny C. Pro tuto úlohu připravte data tak, aby výsledná data mohla být použita dolovacím algoritmem. Tzn. připravte soubor ve formátu CSV, kde každý řádek bude odpovídat jednomu objektu, každý sloupec nějakému atributu. Dále pak ve vybraných datech detekujte odlehlé hodnoty a nahraďte je jinou vhodnou hodnotou, pro jeden zvolený sloupec proveďte normalizaci hodnot a pro jiný sloupec diskretizaci hodnot. Opět implementujte nástroj, který potřebná data extrahuje z úložiště vytvořeného v první části projektu a dále je požadovaným způsobem upraví. Samotné dolování z dat není vyžadováno.

## Dotazy skupiny A
* Vytvořte krabicové grafy zobrazující rozložení věku nakažených osob v jednotlivých krajích.
   * Přehled osob s prokázanou nákazou dle krajů: https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv
   * Kraje (kód-název): https://www.czso.cz/csu/czso/klasifikace-uzemnich-statistickych-jednotek-cz-nuts, csv: [urllllll](http://stistko.uiv.cz/katalog/ciselnik11.asp?idc=AKEN&ciselnik=%DAzemn%ED%20statistick%E9%20jednotky%20(CZ-NUTS)%20podle%20EU&aap=on)
* Vytvořte sérii sloupcových grafů, které zobrazí:
    * 1. graf: počty provedených očkování v jednotlivých krajích (celkový počet od začátku očkování).
    * 2. graf: počty provedených očkování jako v předchozím bodě navíc rozdělené podle pohlaví. Diagram může mít např. dvě části pro jednotlivá pohlaví.
    * 3. graf: Počty provedených očkování, ještě dále rozdělené dle věkové skupiny. Pro potřeby tohoto diagramu postačí 3 věkové skupiny (0-24 let, 25-59, nad 59).
    * Očkovaní (kraj, město, věk, pohlaví): https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-profese.csv

## Dotazy skupiny B

* Vytvořte sérii sloupcových grafů (alespoň 3), které porovnají vývoj různých covidových ukozatelů vámi zvoleného kraj se zbytkem republiky. Jako covidové ukazatele můžete použít: počet nakažených osob, počet hospitalizovaných osob, počet zemřelých, počet očkovaných. Všechny hodnoty uvažujte přepočtené na jednoho obyvatele kraje/republiky. Zobrazte alespoň 12 po sobě jdoucích hodnot (např. hodnoty za poslední rok po měsících).
  * 1. Nakažení, vyléčení, úmrtí kumulativni: https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv
  * 3. Očkovaní viz A

## Dotazy skupiny C

*Zvolte si jednu z dolovacích úloh ze skupiny C. Pro tuto úlohu připravte data tak, aby výsledná data mohla být použita dolovacím algoritmem. Tzn. připravte soubor ve formátu CSV, kde každý řádek bude odpovídat jednomu objektu, každý sloupec nějakému atributu. Dále pak ve vybraných datech detekujte odlehlé hodnoty a nahraďte je jinou vhodnou hodnotou, pro jeden zvolený sloupec proveďte normalizaci hodnot a pro jiný sloupec diskretizaci hodnot. Opět implementujte nástroj, který potřebná data extrahuje z úložiště vytvořeného v první části projektu a dále je požadovaným způsobem upraví. Samotné dolování z dat není vyžadováno.*

* Hledání skupin podobných měst z hlediska vývoje covidu a věkového složení obyvatel.
  * Atributy: počet nakažených za poslední 4 čtvrtletí, počet očkovaných za poslední 4 čtvrtletí, počet obyvatel ve věkové skupině 0..14 let, počet obyvatel ve věkové skupině 15 - 59, počet obyvatel nad 59 let.
  * Pro potřeby projektu vyberte libovolně 50 měst, pro které najdete potřebné hodnoty (můžete např. využít nějaký žebříček 50 nejlidnatějších měst v ČR).

  * Očkovaní viz A
  * Obyvatelstvo podle pětiletých věkových skupin a pohlaví v krajích a okresech: https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv/760fab9c-d079-4d3a-afed-59cbb639e37d?version=1.1
