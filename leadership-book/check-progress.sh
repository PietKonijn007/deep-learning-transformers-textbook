#!/bin/bash

# Progress Checker for Leadership Book Generation
# Usage: ./check-progress.sh

echo "================================================"
echo "Leadership Book Generation - Progress Report"
echo "================================================"
echo ""

# Count tasks
TOTAL_TASKS=$(grep -c "^\- \[.\]" tasks/TASK_BREAKDOWN.md)
COMPLETED_TASKS=$(grep -c "^\- \[x\]" tasks/TASK_BREAKDOWN.md)
REMAINING_TASKS=$((TOTAL_TASKS - COMPLETED_TASKS))
PERCENT=$((COMPLETED_TASKS * 100 / TOTAL_TASKS))

echo "Overall Progress:"
echo "  Total Tasks: $TOTAL_TASKS"
echo "  Completed: $COMPLETED_TASKS ($PERCENT%)"
echo "  Remaining: $REMAINING_TASKS"
echo ""

# Count chapters
CHAPTER_FILES=$(ls -1 chapters/chapter*.tex 2>/dev/null | wc -l)
echo "Chapter Files Created: $CHAPTER_FILES / 24"
echo ""

# Count diagram prompt files
DIAGRAM_PROMPTS=$(ls -1 tasks/chapter*_diagrams.md 2>/dev/null | wc -l)
echo "Diagram Prompt Files: $DIAGRAM_PROMPTS / 24"
echo ""

# Count diagram files
DIAGRAM_FILES=$(ls -1 chapters/diagrams/*.svg 2>/dev/null | wc -l)
echo "Diagram Files Generated: $DIAGRAM_FILES"
echo ""

# Phase breakdown
echo "Phase Status:"
echo "  Phase 1 (Setup): ✅ Complete"

PHASE2=$(grep -A 20 "### Phase 2:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[x\]")
PHASE2_TOTAL=$(grep -A 20 "### Phase 2:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[.\]")
echo "  Phase 2 (Part I): $PHASE2 / $PHASE2_TOTAL tasks"

PHASE3=$(grep -A 30 "### Phase 3:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[x\]")
PHASE3_TOTAL=$(grep -A 30 "### Phase 3:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[.\]")
echo "  Phase 3 (Part II): $PHASE3 / $PHASE3_TOTAL tasks"

PHASE4=$(grep -A 25 "### Phase 4:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[x\]")
PHASE4_TOTAL=$(grep -A 25 "### Phase 4:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[.\]")
echo "  Phase 4 (Part III): $PHASE4 / $PHASE4_TOTAL tasks"

PHASE5=$(grep -A 30 "### Phase 5:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[x\]")
PHASE5_TOTAL=$(grep -A 30 "### Phase 5:" tasks/TASK_BREAKDOWN.md | grep -c "^\- \[.\]")
echo "  Phase 5 (Part IV): $PHASE5 / $PHASE5_TOTAL tasks"

echo ""

# Next task
echo "Next Task:"
NEXT_TASK=$(grep -m 1 "^\- \[ \]" tasks/TASK_BREAKDOWN.md | sed 's/^- \[ \] //')
echo "  $NEXT_TASK"
echo ""

# Recent files
echo "Recently Modified Files:"
ls -lt leadership-book/{chapters,tasks}/*.{tex,md} 2>/dev/null | head -5 | awk '{print "  " $9 " (" $6 " " $7 ")"}'
echo ""

echo "================================================"
echo "Run 'cat tasks/TASK_BREAKDOWN.md' for full details"
echo "================================================"
