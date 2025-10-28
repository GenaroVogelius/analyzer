import { useDeleteOperations } from "@/api/Operations/Operations.delete.api";
import { Button } from "@/components/ui/button";
import type { RowModel } from "@tanstack/react-table";

export interface RowSelectorProps {
  tableFilteredSelectedRowModel: RowModel<any>;
  tableFilteredRowModel: RowModel<any>;
  hasDeleteButton?: boolean;
}

export function RowSelector({
  tableFilteredSelectedRowModel,
  tableFilteredRowModel,
  hasDeleteButton = false,
}: RowSelectorProps) {
  const { mutate: deleteOperations } = useDeleteOperations();

  const handleDeleteOperation = () => {
    const selectedIds = tableFilteredSelectedRowModel.rows.map(
      (row) => row.original.id
    );
    deleteOperations(selectedIds);
  };

  const isDeleteOperationDisabled =
    tableFilteredSelectedRowModel.rows.length === 0;
  return (
    <div className="text-muted-foreground flex-1 text-sm flex flex-col sm:flex-row items-center gap-2">
      {tableFilteredSelectedRowModel.rows.length} de{" "}
      {tableFilteredRowModel.rows.length} fila(s) seleccionada(s).
      {hasDeleteButton && (
        <Button
          variant="destructive"
          size="sm"
          className="cursor-pointer"
          disabled={isDeleteOperationDisabled}
          onClick={handleDeleteOperation}
        >
          <span className="">Delete Operation</span>
        </Button>
      )}
    </div>
  );
}
