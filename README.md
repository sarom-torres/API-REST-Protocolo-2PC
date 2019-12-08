#Replicação mestre escravo

> Engenharia de Telecomunicações - Sistemas Distribuídos (STD29006)
>
> Instituto Federal de Santa Catarina - campus São José

Neste projeto foi desenvolvida uma API REST para simulação do protocolo 2PC na implementação de log de contas bancárias.
O sistema é composto por três máquinas em que uma assume o papel de coordenador e outras duas assumem o papel de réplicas. 
A aplicação coordenador é responsável pela interação com o usuário e pelo envio de ações para réplicas. As máquinas réplicas
são responsáveis por realizar a votação e persistir os dados atualizados em disco. No final da simulação todas as deverão possuir
mesmos dados em log.

## Definição do projeto

