function [ Pop ] = POP_INICIAL(ind_pop,num_est, num_nos)
% POP_INICIAL - Gera populacao inicial
%     ind_pop - Numero de individuos da popula��o
%     num_est - numero de esta��es de munitoramento
%     num_nos - numero total de n�s da rede
%-------------------------------------------------------
 pop_ini = zeros(ind_pop,num_est);
 %Gera��o dos indivduos da popula��o inicial
 for i=1:1:ind_pop
     gera = randperm(num_nos);
     for j=1:1:num_est
         pop_ini(i,j) = gera(j);
     end
 Pop(i).indice = i;
 Pop(i).cromossomo = pop_ini(i,:);
 POP(i).ajuste = 0;
 end
end

