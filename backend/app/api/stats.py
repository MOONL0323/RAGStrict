"""
统计数据API接口
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.core.database import get_db
from app.models.database import Document, DocumentChunk, Entity, Relation, User, DevType, DocumentType
from app.schemas.stats import DashboardStats, DocumentStats, EntityStats
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """获取仪表板统计数据"""
    try:
        # 文档统计
        total_documents = (await db.execute(select(func.count(Document.id)))).scalar() or 0
        processing_documents = (await db.execute(
            select(func.count(Document.id)).filter(Document.processing_status == 'processing')
        )).scalar() or 0
        completed_documents = (await db.execute(
            select(func.count(Document.id)).filter(Document.processing_status == 'completed')
        )).scalar() or 0
        
        # 文本块统计
        total_chunks = (await db.execute(select(func.count(DocumentChunk.id)))).scalar() or 0
        
        # 实体和关系统计
        total_entities = (await db.execute(select(func.count(Entity.id)))).scalar() or 0
        total_relations = (await db.execute(select(func.count(Relation.id)))).scalar() or 0
        
        # 团队成员统计
        team_members = (await db.execute(
            select(func.count(User.id)).filter(User.is_active == True)
        )).scalar() or 0
        
        # 知识图谱数量（按项目分组计算）
        knowledge_graphs = (await db.execute(
            select(func.count(func.distinct(Document.project_id)))
            .filter(Document.project_id.isnot(None))
        )).scalar() or 0
        
        return DashboardStats(
            totalDocuments=total_documents,
            processingDocuments=processing_documents,
            completedDocuments=completed_documents,
            totalChunks=total_chunks,
            totalEntities=total_entities,
            totalRelations=total_relations,
            teamMembers=team_members,
            knowledgeGraphs=knowledge_graphs
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")

@router.get("/documents", response_model=DocumentStats)
async def get_document_stats(db: AsyncSession = Depends(get_db)):
    """获取文档详细统计"""
    try:
        # 总数统计
        total = (await db.execute(select(func.count(Document.id)))).scalar() or 0
        processing = (await db.execute(
            select(func.count(Document.id)).filter(Document.processing_status == 'processing')
        )).scalar() or 0
        completed = (await db.execute(
            select(func.count(Document.id)).filter(Document.processing_status == 'completed')
        )).scalar() or 0
        failed = (await db.execute(
            select(func.count(Document.id)).filter(Document.processing_status == 'failed')
        )).scalar() or 0
        
        # 按类型统计 - 通过 JOIN DevType 表
        business_docs = (await db.execute(
            select(func.count(Document.id))
            .join(DevType, Document.dev_type_id == DevType.id)
            .filter(DevType.category == DocumentType.BUSINESS_DOC)
        )).scalar() or 0
        demo_code = (await db.execute(
            select(func.count(Document.id))
            .join(DevType, Document.dev_type_id == DevType.id)
            .filter(DevType.category == DocumentType.DEMO_CODE)
        )).scalar() or 0
        
        # 按时间统计（最近7天）
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_uploads = (await db.execute(
            select(func.count(Document.id)).filter(Document.created_at >= seven_days_ago)
        )).scalar() or 0
        
        # 按团队统计
        team_stats_result = await db.execute(
            select(Document.team_id, func.count(Document.id).label('count'))
            .filter(Document.team_id.isnot(None))
            .group_by(Document.team_id)
        )
        team_stats = team_stats_result.all()
        
        team_distribution = {team: count for team, count in team_stats}
        
        return DocumentStats(
            total=total,
            processing=processing,
            completed=completed,
            failed=failed,
            business_docs=business_docs,
            demo_code=demo_code,
            recent_uploads=recent_uploads,
            team_distribution=team_distribution
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档统计失败: {str(e)}")

@router.get("/entities", response_model=EntityStats)
async def get_entity_stats(db: AsyncSession = Depends(get_db)):
    """获取实体统计数据"""
    try:
        # 总数统计
        total_entities = (await db.execute(select(func.count(Entity.id)))).scalar() or 0
        total_relations = (await db.execute(select(func.count(Relation.id)))).scalar() or 0
        
        # 按类型统计实体
        entity_types_result = await db.execute(
            select(Entity.entity_type, func.count(Entity.id).label('count'))
            .group_by(Entity.entity_type)
        )
        entity_types = entity_types_result.all()
        
        entity_type_distribution = {entity_type: count for entity_type, count in entity_types}
        
        # 按类型统计关系
        relation_types_result = await db.execute(
            select(Relation.relation_type, func.count(Relation.id).label('count'))
            .group_by(Relation.relation_type)
        )
        relation_types = relation_types_result.all()
        
        relation_type_distribution = {relation_type: count for relation_type, count in relation_types}
        
        return EntityStats(
            total_entities=total_entities,
            total_relations=total_relations,
            entity_type_distribution=entity_type_distribution,
            relation_type_distribution=relation_type_distribution
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取实体统计失败: {str(e)}")

@router.get("/chunks")
async def get_chunk_stats(db: AsyncSession = Depends(get_db)):
    """获取文本块统计"""
    try:
        total = (await db.execute(select(func.count(DocumentChunk.id)))).scalar() or 0
        
        # 按文档类型统计 - 通过 JOIN DevType 表
        chunk_stats_result = await db.execute(
            select(
                DevType.category,
                func.count(DocumentChunk.id).label('chunk_count'),
                func.avg(func.length(DocumentChunk.content)).label('avg_length')
            )
            .join(DocumentChunk, Document.id == DocumentChunk.document_id)
            .join(DevType, Document.dev_type_id == DevType.id)
            .group_by(DevType.category)
        )
        chunk_stats = chunk_stats_result.all()
        
        type_distribution = {}
        avg_lengths = {}
        
        for doc_type, chunk_count, avg_length in chunk_stats:
            type_distribution[doc_type] = chunk_count
            avg_lengths[doc_type] = round(avg_length or 0)
        
        return {
            "total": total,
            "type_distribution": type_distribution,
            "avg_lengths": avg_lengths
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文本块统计失败: {str(e)}")

@router.get("/users")
async def get_user_stats(db: AsyncSession = Depends(get_db)):
    """获取用户统计"""
    try:
        total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
        active_users = (await db.execute(
            select(func.count(User.id)).filter(User.is_active == True)
        )).scalar() or 0
        
        # 按角色统计
        role_stats_result = await db.execute(
            select(User.role, func.count(User.id).label('count'))
            .group_by(User.role)
        )
        role_stats = role_stats_result.all()
        
        role_distribution = {role: count for role, count in role_stats}
        
        # 最近注册用户（30天内）
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_registrations = (await db.execute(
            select(func.count(User.id)).filter(User.created_at >= thirty_days_ago)
        )).scalar() or 0
        
        # 活跃项目数（有文档上传的项目）
        active_projects = (await db.execute(
            select(func.count(func.distinct(Document.project_id)))
            .filter(Document.project_id.isnot(None))
        )).scalar() or 0
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "role_distribution": role_distribution,
            "recent_registrations": recent_registrations,
            "active_projects": active_projects
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户统计失败: {str(e)}")


@router.get("/knowledge-base")
async def get_knowledge_base_stats(db: AsyncSession = Depends(get_db)):
    """
    获取知识库统计 - 为MCP服务器提供知识库总览
    """
    try:
        # 文档总数
        total_documents = (await db.execute(select(func.count(Document.id)))).scalar() or 0
        
        # 文本块总数
        total_chunks = (await db.execute(select(func.count(DocumentChunk.id)))).scalar() or 0
        
        # 实体和关系总数
        total_entities = (await db.execute(select(func.count(Entity.id)))).scalar() or 0
        total_relations = (await db.execute(select(func.count(Relation.id)))).scalar() or 0
        
        # 按编程语言分类 (从 dev_type 推断)
        languages_query = select(DevType.name).distinct()
        languages_result = await db.execute(languages_query)
        languages = [row[0] for row in languages_result.all()]
        
        # 团队列表
        from app.models.database import Team
        teams_query = select(Team.name)
        teams_result = await db.execute(teams_query)
        teams = [row[0] for row in teams_result.all()]
        
        # 项目列表
        from app.models.database import Project
        projects_query = select(Project.name)
        projects_result = await db.execute(projects_query)
        projects = [row[0] for row in projects_result.all()]
        
        return {
            "success": True,
            "data": {
                "total_documents": total_documents,
                "total_chunks": total_chunks,
                "total_entities": total_entities,
                "total_relations": total_relations,
                "languages": languages,
                "teams": teams,
                "projects": projects,
                "last_updated": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识库统计失败: {str(e)}")