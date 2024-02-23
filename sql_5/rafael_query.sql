-- Esse codigo foi feito utilizando o MySQL
-- É necessário que seja rodado primeiramente o script contendo a criação do bd e da tabela "comissoes"

-- A ideia aqui foi de criar uma tabela temporaria contendo a coluna vendedor, valor e o número da linha
-- O número de linha foi adicionado utilizando a função row_number, sendo ordenado de forma decrescente
-- De forma com que o maior valor para cada vendedor estaria na linha de index 1 e a menor com index 4

CREATE TEMPORARY TABLE IF NOT EXISTS maiores_valores AS 
(SELECT vendedor, valor, ROW_NUMBER() OVER (PARTITION BY vendedor ORDER BY valor DESC) AS row_num FROM comissoes);

-- Uma vez que a tabela temporária foi criada, foi possível utilizar um simples where para limitar as linhas
-- Eliminando as linhas em que o index fosse maior que 3, pegando assim só os 3 maiores valores
-- Um group by com a soma de valores maiores ou iguais a 1024 para finalmente encontrar os vendedores

SELECT vendedor, SUM(valor) as soma_valor FROM maiores_valores WHERE row_num <= 3
GROUP BY vendedor HAVING SUM(valor) >= 1024 order by vendedor asc;




