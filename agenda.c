#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>

struct item_agenda {
       int codigo; //numero sequencial gerado pelo programa
       char nome[100];
       struct telefones {
              char fixo[20];
              char celular[20];
              char comercial[20];
       } fone;
};

//   pesquisa de substring como o nome de inicio para comparar
//   compara uma determinada quantidade de chars
//   compara não case sensitive
//   sub Pedro, str Pedro da Silva  strlen(sub) retorna igual
//   retorna 0 se igual e 1 se diferente
int pesquisaSub(const char *sub, const char *str) {
    return (strncasecmp(sub,str,strlen(sub)));
}

//   vai para o inicio do arquivo e tenta ler
//   se não erro retorna o valor de seq

int getSequencial(FILE* fp) {
    int seq;

    rewind(fp);
    if (fread(&seq,sizeof(int),1,fp) != 1) {
       seq = 0;
       rewind(fp);
       fwrite(&seq,sizeof(int),1,fp);
    }
    return seq;
}

//   monta uma nova struct e retorna esse elemento
struct item_agenda leDados(FILE* fp) {
    struct item_agenda novo;
    int seqAtual;

    seqAtual = getSequencial(fp);
    novo.codigo = seqAtual+1;
    printf("\nCodigo: %d",novo.codigo);

    printf("\nNome: ");
    gets(novo.nome);
    printf("\nTel.Fixo: ");
    gets(novo.fone.fixo);
    printf("\nTel.Celular: ");
    gets(novo.fone.celular);
    printf("\nTel.Comercial: ");
    gets(novo.fone.comercial);

    return novo;
}


//   função que grava os dados lidos
//   inicio do arquivo pula seq
//  atualiza o novo seq
void incluiContato(FILE *fp) {
    struct item_agenda novo;
    int seq;

    novo = leDados(fp);

    rewind(fp);
    fread(&seq,sizeof(int),1,fp);

    fseek(fp,(seq)*sizeof(novo),SEEK_CUR);
    fwrite(&novo,sizeof(novo),1,fp);

    rewind(fp);
    fwrite(&novo.codigo,sizeof(int),1,fp);

}
//   lista todos os contatos
//   lendo em um while até não ter mais o que ler

void listarContatos(FILE *fp) {
    struct item_agenda lido;
    int seq;

    rewind(fp);

    fread(&seq,sizeof(int),1,fp); //Pula o sequencial

    while(fread(&lido,sizeof(lido),1,fp)) {
        printf("\nCodigo: %d",lido.codigo);
        printf("\nNome: %s",lido.nome);
        printf("\nTel.Celular: %s",lido.fone.celular);
        printf("\nTel.Fixo: %s",lido.fone.fixo);
        printf("\nTel.Comercial: %s",lido.fone.comercial);
        printf("\n\n");
    }
}

//   consultar pelo nome
//   leio o nome
//   se estiver 5 pedro s ele imprime os 5 pedros
//   se naõ achou 0
void consultarNome(FILE *fp) {
     char snome[150];
     int seq;
     int achou = 0;
     struct item_agenda lido;

     printf("\n\nNome: ");
     gets(snome);

     rewind(fp);

     fread(&seq,sizeof(int),1,fp); //Pula o sequencial

     while(fread(&lido,sizeof(lido),1,fp)) {
        //if (strcmp(lido.nome,snome)==0) {
        if (pesquisaSub(snome,lido.nome)==0) {
           printf("\nCodigo: %d",lido.codigo);
           printf("\nNome: %s",lido.nome);
           printf("\nTel.Celular: %s",lido.fone.celular);
           printf("\nTel.Fixo: %s",lido.fone.fixo);
           printf("\nTel.Comercial: %s",lido.fone.comercial);
           printf("\n\n");
           achou = 1;
        }
     }
     if (!achou) {
         printf("\n\nNenhum %s foi encontrado!\n\n",snome);
     }
}

//    consultar pelo código
//    usar fflush(stdin) para limpar o buffer
//    pula-se o seq
//   leo dados e imp´rime se igual
void consultarCodigo(FILE *fp) {
     char scod;
     int seq;
     struct item_agenda lido;

     printf("\n\nCodigo: ");
     scanf("%d",&scod);
     fflush(stdin);

     rewind(fp);
     fread(&seq,sizeof(int),1,fp); //Pula o sequencial

     fseek(fp,(scod-1)*sizeof(lido),SEEK_CUR);

     if (fread(&lido,sizeof(lido),1,fp)) {
         printf("\nCodigo: %d",lido.codigo);
         printf("\nNome: %s",lido.nome);
         printf("\nTel.Celular: %s",lido.fone.celular);
         printf("\nTel.Fixo: %s",lido.fone.fixo);
         printf("\nTel.Comercial: %s",lido.fone.comercial);
         printf("\n\n");
     } else {
         printf("\n\nElemento nao encontrado!\n\n");
     }
}
//   le e volta para o inicio
void alterarCodigo(FILE *fp) {
     int scod;
     int seq;
     struct item_agenda lido;

     printf("\n\nCodigo: ");
     scanf("%d",&scod);
     fflush(stdin);

     rewind(fp);
     fread(&seq,sizeof(int),1,fp); //Pula o sequencial
     fseek(fp,(scod-1)*sizeof(lido),SEEK_CUR);

     if (fread(&lido,sizeof(lido),1,fp)) {
         printf("\nCodigo: %d",lido.codigo);
         printf("\nNome: %s",lido.nome);
         printf("\nTel.Celular: %s",lido.fone.celular);
         printf("\nTel.Fixo: %s",lido.fone.fixo);
         printf("\nTel.Comercial: %s",lido.fone.comercial);
         printf("\n\n");

        //   nova struct faz com que o codigo seja o mesmo
        //   se o usuario nao quiser alterar um campo simplismente digite enter
        //   ai pode alterar somemte o necessario
        struct item_agenda novo;
        char resposta;

        novo.codigo = lido.codigo;
        printf("\nNome: ");
        gets(novo.nome);
        if (strlen(novo.nome)==0) {
           strcpy(novo.nome,lido.nome);
        }
        printf("\nTel.Fixo: ");
        gets(novo.fone.fixo);
        if (strlen(novo.fone.fixo)==0) {
           strcpy(novo.fone.fixo,lido.fone.fixo);
        }
        printf("\nTel.Celular: ");
        gets(novo.fone.celular);
        if (strlen(novo.fone.celular)==0) {
           strcpy(novo.fone.celular,lido.fone.celular);
        }
        printf("\nTel.Comercial: ");
        gets(novo.fone.comercial);
        if (strlen(novo.fone.comercial)==0) {
           strcpy(novo.fone.comercial,lido.fone.comercial);
        }

        printf("\n\nConfirma as alterações para este registro? (y/n)");
        resposta = getch();
        //   casdo o chiru quizer alterar ele altera se naõ pula fora do laço
        switch (resposta) {
               case 'Y':
               case 'y':  rewind(fp);
                          fread(&seq,sizeof(int),1,fp); //Pula o sequencial
                          fseek(fp,(scod-1)*sizeof(lido),SEEK_CUR);
                          fwrite(&novo,sizeof(novo),1,fp);
                          printf("\n\nRegistro alterado com sucesso.");
                          break;
               case 'N':
               case 'n':  printf("\n\nRegistro nao alterado.");
                          break;
               default: printf("\n\nOpcao invalida! Registro nao alterado.");
        }

     } else {
         printf("\n\nElemento nao encontrado!\n\n");
     }

}

//   struct basica de menu
char showMenu() {
     char opcao;
     opcao = '0';
     do {
         printf("\n\n");
         printf("\n1 - Incluir");
         printf("\n2 - Alterar");
         printf("\n3 - Excluir (nao implementado)");
         printf("\n4 - Consultar pelo Nome");
         printf("\n5 - Consultar pelo Codigo");
         printf("\n6 - Listar");
         printf("\n7 - Sair");
         printf("\n\nDigite a opcao desejada: ");
         opcao = getc(stdin);
         fflush(stdin);
     } while (!((opcao >= '1')&&(opcao <= '7')));
     return opcao;
}

//   se o arquivo não existe ele é recriado
int main() {
    char op;
    FILE* fp;

    if ((fp = fopen("agenda.dat","rb+")) == NULL) {
            printf("\n\nArquivo nao encontrado.\n\n");
            printf("\n\nRecriando o arquivo...\n\n");
            fp = fopen("agenda.dat","wb+");
            printf("\n\nArquivo recriado.\n\n");
            system("PAUSE");
    }

    do {
        switch (op = showMenu()) {
           case '1': incluiContato(fp);
                     break;
           case '2': alterarCodigo(fp);
                     break;
           case '3': //Exclusao (nao implementado)
                     break;
           case '4': consultarNome(fp);
                     break;
           case '5': consultarCodigo(fp);
                     break;
           case '6': listarContatos(fp);
                     break;
           case '7': break;
        }
        printf("\n\nPressione qualquer tecla para continuar...");
        getch();
        system("CLS");
    } while (op != '7');
    system("PAUSE");
}
