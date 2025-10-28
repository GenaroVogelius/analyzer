import { TableCell, TableRow } from "@/components/ui/table";
import type { PositionsColumnsType } from "@/features/DataTables/PositionsTable/PositionsColumns/operations/PositionsColumns";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import type { Row } from "@tanstack/react-table";
import { flexRender } from "@tanstack/react-table";
// import { ExpandedRowContent } from "@/features/DataTables/PositionsTable/components/ExpandedRowContent";
import { PositionsExpandedTable } from "@/features/DataTables/PositionsExpandedTable";
import { PositionsExpandedColumns } from "@/features/DataTables/PositionsExpandedTable/PositionsExpandedColumns";

export function DraggableRow({ row }: { row: Row<PositionsColumnsType> }) {
  const { transform, transition, setNodeRef, isDragging } = useSortable({
    id: row.original.id,
  });

  // Si es una sub-fila, no renderizar nada (las sub-filas se manejan automáticamente)
  if ((row.original as any).isSubRow) {
    return null;
  }

  return (
    <>
      <TableRow
        data-state={row.getIsSelected() && "selected"}
        data-dragging={isDragging}
        ref={setNodeRef}
        className="relative z-0 data-[dragging=true]:z-10 data-[dragging=true]:opacity-80"
        style={{
          transform: CSS.Transform.toString(transform),
          transition: transition,
        }}
      >
        {row.getVisibleCells().map((cell) => (
          <TableCell key={cell.id}>
            {flexRender(cell.column.columnDef.cell, cell.getContext())}
          </TableCell>
        ))}
      </TableRow>
      {row.getIsExpanded() && row.original.moreInfo && (
        <TableRow>
          <TableCell colSpan={row.getVisibleCells().length} className="p-0">
            {/* <ExpandedRowContent row={row.original} /> */}
            <PositionsExpandedTable
              data={row.original.moreInfo}
              columns={PositionsExpandedColumns}
            />
          </TableCell>
        </TableRow>
      )}
    </>
  );
}
