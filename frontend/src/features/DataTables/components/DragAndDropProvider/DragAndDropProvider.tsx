import { closestCenter, DndContext, type DragEndEvent } from "@dnd-kit/core";
import { restrictToVerticalAxis } from "@dnd-kit/modifiers";
import * as React from "react";

interface DragAndDropProviderProps {
  children: React.ReactNode;
  handleDragEnd: (event: DragEndEvent) => void;
  sensors: any[];
  sortableId: string;
}

export function DragAndDropProvider({
  children,
  handleDragEnd,
  sensors,
  sortableId,
}: DragAndDropProviderProps) {
  return (
    <DndContext
      collisionDetection={closestCenter}
      modifiers={[restrictToVerticalAxis]}
      onDragEnd={handleDragEnd}
      sensors={sensors}
      id={sortableId}
    >
      {children}
    </DndContext>
  );
}
