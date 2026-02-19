#!/bin/bash
# 🤖 RAG Auto-Indexer Script

CONFIG_FILE=".gemini/anti_gravity/global_skills/rag-auto-indexer/resources/index_config.json"
TARGET_FILE=$(grep -o '"target_memory": "[^"]*"' $CONFIG_FILE | cut -d'"' -f4)

echo "# Knowledge Map v1.1 - Updated by rag-auto-indexer" > $TARGET_FILE
echo "## Last Indexing: $(date)" >> $TARGET_FILE
echo "" >> $TARGET_FILE

# List of sources from config
SOURCES=(".agent-os" ".aitk" ".mem0")

for SRC in "${SOURCES[@]}"; do
    echo "### Source: $SRC" >> $TARGET_FILE
    find "$HOME/$SRC" -maxdepth 2 -not -path '*/.*' >> $TARGET_FILE
    echo "" >> $TARGET_FILE
done

echo "✅ Indexing complete. Knowledge map updated at $TARGET_FILE"
