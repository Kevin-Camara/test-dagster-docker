import dagster as dg
import pandas as pd
import os


particoes = dg.DynamicPartitionsDefinition(name="arquivos")

@dg.asset()
def get_name_files(context: dg.AssetExecutionContext) -> list[str]:
    context.log.info("Identificando arquivos csv armazenados")
    archives_path = "/app/archives"
    csv_files = []
    for file_name in os.listdir(archives_path):
        if file_name.endswith(".csv"):
            full_path = os.path.join(archives_path, file_name)
            csv_files.append(full_path)
   
    context.instance.add_dynamic_partitions(
    partitions_def_name="arquivos",
    partition_keys=csv_files
    )
    return csv_files

@dg.asset(deps=[get_name_files], partitions_def=particoes)
def get_data_brick_iqvia(context: dg.AssetExecutionContext) -> pd.DataFrame:
    arquivo = context.partition_key

    context.log.info(f"Processando arquivo: {arquivo}")
    
    df: pd.DataFrame = pd.read_csv(arquivo, sep=';', decimal=',')
    
    context.add_output_metadata({
    "num_rows": len(df),
    "partition": arquivo
    })
    return df



@dg.asset_check(asset=get_data_brick_iqvia)
def check_columns_brick_iqvia(get_data_brick_iqvia) -> dg.AssetCheckResult:

    failed_partitions = []
    
    waiting_columns = ['produto', 'so', 'si', 'interno']

    for partition_key, df in get_data_brick_iqvia.items():
        missing_columns = [col for col in waiting_columns if col not in df.columns]

        if missing_columns:
            failed_partitions.append({
                "partition": partition_key,
                "missing_columns": missing_columns
            })

    # Se alguma partição falhou, o check deve retornar como "FAILED"
    if failed_partitions:
        message = (
            f"As seguintes partições estão faltando colunas obrigatórias:\n"
            + "\n".join(
                [f"- {f['partition']}: faltando {', '.join(f['missing_columns'])}" for f in failed_partitions]
            )
        )
        return dg.AssetCheckResult(
            passed=False,
            metadata={"failed_partitions": failed_partitions},
            description=message
        )

    # Caso contrário, o check passou com sucesso
    return dg.AssetCheckResult(
        passed=True,
        description="Todas as partições possuem as colunas obrigatórias."
    )


@dg.definitions
def defs():
    return dg.Definitions(
        assets=[get_name_files, get_data_brick_iqvia],
        asset_checks=[check_columns_brick_iqvia]
    )
