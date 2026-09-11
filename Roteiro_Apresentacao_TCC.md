# Roteiro de Apresentação — TCC (15 minutos)
### Pipeline de Análise de Dados Reprodutivos para Gestão de Rebanho Bovino

---

## [0:00–1:30] Abertura — a promessa

Boa tarde a todos. Antes de entrar nos detalhes técnicos, eu quero contar uma cena bem comum no interior do Brasil.

Um produtor rural tem um caderno velho, cheio de anotações sobre as vacas dele: quando pariu, quantos bezerros nasceram, quais são macho e quais são fêmea. Só que o caderno vai se desgastando. A letra fica difícil de ler. Em algum momento, ele para de anotar. Outros produtores tentam substituir o caderno por foto no celular, ou por conversa de WhatsApp — e o resultado é o mesmo: a informação some com o tempo, e ninguém consegue responder, com segurança, uma pergunta simples: como está o desempenho reprodutivo do meu rebanho?

Nos próximos 15 minutos, eu vou mostrar como peguei justamente esse tipo de registro bagunçado — de uma propriedade real — e transformei ele em um painel visual que qualquer produtor consegue entender, sem precisar mexer em planilha nenhuma. Essa é a promessa deste trabalho, e é ela que eu vou cumprir até o final desta apresentação.

## [1:30–3:00] O problema

Existem três jeitos bem comuns de controlar rebanho de forma informal, e os três falham do mesmo jeito, com o tempo.

O primeiro é o caderno de papel, que já expliquei: ele se perde, rasga, e a letra apaga.

O segundo é confiar só na memória, apoiada em foto. O produtor tira uma foto do bezerro e espera lembrar depois, de cabeça, de quem é a mãe, quando nasceu, se é macho ou fêmea. Não existe nenhum dado escrito junto da imagem — só a lembrança de quem tirou a foto.

O terceiro é o WhatsApp, hoje o aplicativo mais usado no campo. O problema é que conversa antiga se apaga, às vezes sem querer, e a informação que estava ali dentro some junto.

Diante disso, o problema deste trabalho pode virar uma pergunta única: como transformar anotações soltas e sem padrão em informação organizada e confiável, de um jeito automático, sem depender do produtor mexer em planilha toda vez que precisar consultar um dado?

## [3:00–4:00] Objetivo

O objetivo geral deste trabalho foi criar um pipeline — ou seja, uma sequência automática de passos — que pegasse esses dados brutos de vacas, touros e partos, e transformasse tudo em indicadores úteis para a gestão do rebanho. E esse resultado deveria ficar disponível de duas formas: guardado em um banco de dados, e mostrado em um painel visual interativo.

Só que ter esse objetivo no papel é fácil. Difícil é construir algo que realmente funcione em cima de dados reais e bagunçados. E é exatamente daí que vem a próxima parte: de onde vieram esses dados, e por que escolhi as ferramentas que escolhi.

## [4:00–6:00] Os dados e as ferramentas

Os dados deste trabalho não são fictícios. Eles vêm de uma planilha real, de uma pequena propriedade rural, dividida em três abas: uma com 16 vacas, outra com 1 touro, e outra com 12 partos registrados.

E antes que alguém pergunte: sim, essa é uma base pequena — e não, esse número não foi uma escolha minha. É o tamanho real do rebanho estudado. É justamente esse tipo de base pequena e desorganizada, do jeito que ela existe na vida real, que motiva o trabalho inteiro. Trabalhar com dado perfeito não representaria o problema que eu me propus a resolver.

E o problema, de fato, apareceu: nomes de coluna diferentes em cada aba para representar a mesma coisa, datas em formatos diferentes, sexo da cria escrito como "M", "m" e "Macho" ao mesmo tempo, e um parto sem nenhuma vaca vinculada a ele.

Para tratar isso, escolhi ferramentas gratuitas de propósito: Python para o código, SQLite como banco de dados, e Power BI para o painel final. Não escolhi o SQLite porque ele é o banco mais avançado do mercado — ele nem é. Escolhi porque ele não pede instalação nem servidor: é um arquivo só. Isso importa porque quem vai usar esse projeto, no fim das contas, não é um data center. É uma propriedade pequena, com pouco recurso técnico.

Só que ter os dados e escolher as ferramentas certas ainda não resolve nada sozinho. Falta o processo que liga tudo isso — e é sobre esse processo que eu vou falar agora.

## [6:00–9:00] Como o pipeline funciona

O pipeline foi dividido em cinco passos, um depois do outro.

O primeiro passo só organiza as pastas do projeto, garantindo que tudo tenha um lugar certo antes de começar.

O segundo passo é onde a bagunça começa a ser resolvida: a planilha é lida, os nomes de coluna são padronizados, os tipos de dado são corrigidos, e o texto é uniformizado — é aqui, por exemplo, que "M", "m" e "Macho" viram todos a mesma coisa.

O terceiro passo carrega esses dados já tratados dentro do banco SQLite, e faz uma verificação importante: quantos partos ficaram corretamente ligados a uma vaca, e quantos ficaram órfãos, sem vínculo nenhum. Essa verificação, sozinha, já vale a pena: foi ela que encontrou, de forma automática, o parto sem vaca vinculada que citei há pouco — algo que passaria despercebido numa planilha manual.

O quarto passo calcula os indicadores, por meio de consultas SQL: o ranking de partos por vaca, e a proporção de machos e fêmeas entre as crias.

E o quinto passo transforma esses indicadores em gráficos, e exporta tudo — dados e gráficos juntos — numa planilha Excel pronta para alimentar o painel no Power BI.

Só que descrever um processo não é o mesmo que provar que ele funciona. A pergunta que interessa agora não é como o pipeline foi construído, e sim: o que ele encontrou, de fato, quando rodei ele em cima dos dados reais da propriedade?

## [9:00–11:30] O que os números mostraram

Depois do tratamento, 11 dos 12 partos ficaram corretamente vinculados a uma vaca. O parto órfão foi mantido no banco, mas excluído do cálculo, porque não dá para atribuir ele a nenhum animal específico.

Entre essas 11, uma vaca se destacou: a Boneca, com 2 partos registrados. As outras 9 vacas com pelo menos um parto aparecem empatadas, com 1 parto cada.

Na proporção de sexo, o resultado foi 7 crias macho e 4 crias fêmea, entre os 11 partos válidos. Isso dá 63,6% de machos contra 36,4% de fêmeas nesta base.

E, antes que perguntem: não, isso não é uma conclusão sobre gado brasileiro em geral. É um fato sobre esta propriedade, com esta amostra pequena. Eu volto nesse ponto daqui a pouco, com mais cuidado.

Todos esses números foram reunidos num painel do Power BI, com quatro elementos: o gráfico de ranking por vaca, o gráfico de proporção de sexo, e dois cartões numéricos — total de partos válidos, e quantidade de vacas com pelo menos um parto.

Só que mostrar um número bonito na tela não prova, sozinho, que ele está correto. Antes de fechar, eu queria ter certeza de que cada valor batia com a realidade dos dados. Foi isso que eu fiz na etapa seguinte.

## [11:30–13:00] Como eu sei que os números estão certos

Eu validei o pipeline em três níveis.

O primeiro nível confere se a leitura dos dados bateu: 16 vacas, 1 touro e 12 partos lidos, exatamente como na planilha original.

O segundo nível é uma conferência manual do ranking. Eu contei, à mão, os partos por vaca na planilha já tratada, e o resultado bateu com o que o pipeline calculou: Boneca com 2 partos, as outras 9 com 1 parto cada.

O terceiro nível refaz, à mão, a conta da proporção de sexo: 7 dividido por 11 dá 63,6%, e 4 dividido por 11 dá 36,4%. A soma dá 100%, e os dois valores batem com o que o pipeline apresentou.

Esses três níveis de conferência não eliminam a limitação da amostra pequena — isso eu não escondo. Mas provam algo diferente, e igualmente importante: que o pipeline lê, limpa, relaciona e calcula os dados de forma consistente com a conferência manual. Ou seja, o processo funciona.

Com os resultados já validados, dá para voltar à pergunta que abriu esta apresentação.

## [13:00–15:00] Conclusão — a promessa cumprida

Eu prometi mostrar como transformar um registro bagunçado, de uma propriedade real, em um painel visual que qualquer produtor entende, sem precisar mexer em planilha nenhuma. E foi exatamente isso que aconteceu: os dados soltos das três abas viraram um banco de dados organizado, viraram indicadores calculados por SQL, viraram gráficos, e viraram um painel pronto no Power BI.

Agora, sendo honesto com vocês: esse trabalho tem limites, e eu prefiro deixar isso claro em vez de esconder.

A amostra é pequena — 16 vacas e 12 partos — e isso não permite tirar conclusão nenhuma sobre outros rebanhos, só sobre esta propriedade. Dois indicadores importantes, o Intervalo Entre Partos e a sazonalidade dos partos, não entraram na versão final, porque, entre as 16 vacas, só uma teve mais de um parto registrado — não dava para calcular esses dois números de um jeito que fizesse sentido. E o dashboard, hoje, ainda precisa ser atualizado manualmente no Power BI Desktop toda vez que o pipeline roda de novo.

Esses limites, aliás, apontam exatamente para o caminho de continuidade: ampliar a base com mais partos e mais propriedades, ligar cada parto ao touro correspondente, e automatizar a atualização do painel.

Mas o ponto central deste trabalho nunca foi produzir uma conclusão zootécnica ampla. Foi provar que dá para construir, com ferramentas gratuitas, um caminho completo — da planilha bagunçada até o painel visual — que devolve para o pequeno produtor rural uma informação que ele, hoje, simplesmente não tem. E essa promessa, eu cumpri.

Muito obrigado.
