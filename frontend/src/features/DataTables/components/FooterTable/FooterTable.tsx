import type { Table } from "@tanstack/react-table";
import { Paginator } from "../Paginator";
import { RowSelector } from "../RowSelector";
import { RowsPerPageSelector } from "../RowsPerPageSelector";

export interface FooterTableProps {
  table: Table<any>;
  hasDeleteButton?: boolean;
}

export function FooterTable({ table, hasDeleteButton = false }: FooterTableProps) {
  const setPageSize = (pageSize: number) => {
    table.setPageSize(pageSize);
  };

  return (
    <div className="flex items-center justify-between px-4 flex-col md:flex-row gap-2">
      <RowSelector
        tableFilteredSelectedRowModel={table.getSelectedRowModel()}
        tableFilteredRowModel={table.getRowModel()}
        hasDeleteButton={hasDeleteButton}
      />
      <div className="flex w-full items-center gap-8 lg:w-fit">
        <RowsPerPageSelector
          tableState={table.getState()}
          setPageSize={setPageSize}
        />
        <Paginator table={table} />
      </div>
    </div>
  );
}
