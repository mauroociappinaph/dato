---
name: visual-learning-engine
description: AI-powered visual learning and pattern recognition for autonomous agents. Analyzes screenshots, videos, and visual content to learn workflows, UI patterns, and design principles.
inherited_from: [gemini-skill-creator, ai-engineer, memory-systems]
---

# Visual Learning Engine (Compressed)

## Purpose
Enable autonomous agents to learn from visual content (images, videos, screenshots) and apply learned patterns to improve task execution, design decisions, and user experience optimization.

## Core Capabilities
- **Screenshot Analysis**: Extract UI/UX patterns, workflows, and design principles from application screenshots
- **Video Learning**: Process tutorial videos to understand step-by-step processes and workflows
- **Visual Pattern Recognition**: Identify recurring design patterns and architectural approaches
- **Contextual Learning**: Combine visual insights with textual knowledge for multimodal understanding
- **Memory Integration**: Store visual patterns in vector databases for future retrieval and application

## Integration Points

### Pipeline Integration
- **Step 4.5: Visual Context Injection** - Automatically search and analyze relevant visual examples
- **Step 5.1: Visual-Aware Code Generation** - Generate code considering visual benchmarks
- **Step 8.2: Visual Code Review** - Validate implementations against visual best practices

### Memory Architecture
- **Redis**: Short-term visual pattern cache during task execution
- **Pinecone**: Long-term visual embeddings with semantic search
- **dude-central-brain**: Narrative storage of visual learning experiences

## Technical Implementation

### MCP Dependencies
- **Gemini Vision API**: Core image/video analysis engine
- **Firecrawl**: Automated screenshot capture from web
- **Exa Search**: Find relevant visual content and tutorials

### Data Flow
1. **Input Processing**: Receive task description and identify visual learning needs
2. **Content Discovery**: Search for relevant screenshots, videos, and examples
3. **Visual Analysis**: Extract patterns, workflows, and design principles
4. **Pattern Storage**: Save learnings in multimodal vector database
5. **Context Application**: Inject visual insights into task execution

## Activation Triggers
- Tasks involving "design", "UI", "workflow", "tutorial", "example"
- Projects with visual components (web apps, mobile apps, dashboards)
- Requests for "best practices", "industry standards", "modern approaches"

## Output Formats
- **Pattern Reports**: Structured analysis of visual patterns found
- **Design Recommendations**: UI/UX improvements based on learned patterns
- **Workflow Diagrams**: Visual representations of learned processes
- **Code Examples**: Implementation suggestions with visual context

## Success Metrics
- **Pattern Recognition Accuracy**: >85% correct identification of design patterns
- **Learning Speed**: Reduce time-to-insight by 60% for visual tasks
- **Application Success**: >75% of learned patterns successfully applied to new tasks

## Anti-Patterns to Avoid
- **Over-reliance on Visual**: Don't ignore textual context and documentation
- **Pattern Over-generalization**: Validate patterns against specific use cases
- **Memory Bloat**: Implement efficient caching and cleanup strategies

## Related Skills
- **ai-engineer**: Provides multimodal context for better code generation
- **context7-docs-engine**: Extends documentation search to include visual content
- **google-slides-visual-creator**: Leverages learned visual patterns for presentations
- **memory-systems**: Manages visual pattern storage and retrieval
