import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

ADMIN_PASSWORD = "Exenity@123"

class PurchaseRequest(Base):
    __tablename__ = 'purchase_requests'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    pr_code = Column(String(20), unique=True, nullable=False)
    requester = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    project = Column(String(200), nullable=False)
    item = Column(String(200), nullable=False)
    specification = Column(Text)
    purchase_type = Column(String(50), default='Regular Purchase')
    estimated_cost = Column(Float, default=0)
    actual_cost = Column(Float, default=None, nullable=True)
    priority = Column(String(20), default='Medium')
    status = Column(String(50), default='Pending')
    comments = Column(Text, default='')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.pr_code,
            'requester': self.requester,
            'department': self.department,
            'project': self.project,
            'item': self.item,
            'specification': self.specification or '',
            'purchaseType': self.purchase_type,
            'estimatedCost': self.estimated_cost,
            'actualCost': self.actual_cost,
            'priority': self.priority,
            'status': self.status,
            'comments': self.comments or '',
            'createdAt': self.created_at.isoformat() if self.created_at else ''
        }

Base.metadata.create_all(engine)

def get_next_pr_code():
    session = Session()
    try:
        last_pr = session.query(PurchaseRequest).order_by(PurchaseRequest.id.desc()).first()
        if last_pr:
            next_num = last_pr.id + 1
        else:
            next_num = 1
        return f"PR-{next_num:03d}"
    finally:
        session.close()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/auth/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    password = data.get('password', '')
    if password == ADMIN_PASSWORD:
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid password'}), 401

@app.route('/api/prs', methods=['GET'])
def get_all_prs():
    session = Session()
    try:
        prs = session.query(PurchaseRequest).order_by(PurchaseRequest.id.desc()).all()
        return jsonify([pr.to_dict() for pr in prs])
    finally:
        session.close()

@app.route('/api/prs', methods=['POST'])
def create_pr():
    session = Session()
    try:
        data = request.get_json()
        pr_code = get_next_pr_code()
        
        new_pr = PurchaseRequest(
            pr_code=pr_code,
            requester=data.get('requester', ''),
            department=data.get('department', ''),
            project=data.get('project', ''),
            item=data.get('item', ''),
            specification=data.get('specification', ''),
            purchase_type=data.get('purchaseType', 'Regular Purchase'),
            estimated_cost=float(data.get('estimatedCost', 0) or 0),
            priority=data.get('priority', 'Medium'),
            status='Pending',
            comments=data.get('comments', '')
        )
        
        session.add(new_pr)
        session.commit()
        
        return jsonify({'success': True, 'pr': new_pr.to_dict()}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/prs/<pr_id>/status', methods=['PATCH'])
def update_pr_status(pr_id):
    session = Session()
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        pr = session.query(PurchaseRequest).filter_by(pr_code=pr_id).first()
        if not pr:
            return jsonify({'success': False, 'error': 'PR not found'}), 404
        
        pr.status = new_status
        pr.updated_at = datetime.utcnow()
        session.commit()
        
        return jsonify({'success': True, 'pr': pr.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/prs/<pr_id>/comments', methods=['PATCH'])
def update_pr_comments(pr_id):
    session = Session()
    try:
        data = request.get_json()
        new_comments = data.get('comments', '')
        
        pr = session.query(PurchaseRequest).filter_by(pr_code=pr_id).first()
        if not pr:
            return jsonify({'success': False, 'error': 'PR not found'}), 404
        
        pr.comments = new_comments
        pr.updated_at = datetime.utcnow()
        session.commit()
        
        return jsonify({'success': True, 'pr': pr.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/prs/<pr_id>/actual-cost', methods=['PATCH'])
def update_pr_actual_cost(pr_id):
    session = Session()
    try:
        data = request.get_json()
        actual_cost = data.get('actualCost')
        
        pr = session.query(PurchaseRequest).filter_by(pr_code=pr_id).first()
        if not pr:
            return jsonify({'success': False, 'error': 'PR not found'}), 404
        
        pr.actual_cost = float(actual_cost) if actual_cost else None
        pr.updated_at = datetime.utcnow()
        session.commit()
        
        return jsonify({'success': True, 'pr': pr.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/prs/<pr_id>', methods=['DELETE'])
def delete_pr(pr_id):
    session = Session()
    try:
        pr = session.query(PurchaseRequest).filter_by(pr_code=pr_id).first()
        if not pr:
            return jsonify({'success': False, 'error': 'PR not found'}), 404
        
        session.delete(pr)
        session.commit()
        
        return jsonify({'success': True, 'message': 'PR deleted successfully'})
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/reports/bom-missing', methods=['GET'])
def bom_missing_report():
    session = Session()
    try:
        prs = session.query(PurchaseRequest).filter_by(purchase_type='Missing in BOM').all()
        
        total_cost = sum((pr.actual_cost if pr.actual_cost is not None else 0) for pr in prs)
        pending_count = sum(1 for pr in prs if pr.status == 'Pending')
        approved_count = sum(1 for pr in prs if pr.status in ['Approved', 'In Process', 'Material Received'])
        
        return jsonify({
            'items': [pr.to_dict() for pr in prs],
            'summary': {
                'totalItems': len(prs),
                'totalCost': total_cost,
                'pendingCount': pending_count,
                'approvedCount': approved_count
            }
        })
    finally:
        session.close()

@app.route('/api/reports/expenditure', methods=['GET'])
def expenditure_report():
    session = Session()
    try:
        prs = session.query(PurchaseRequest).all()
        
        def get_cost(pr):
            return pr.actual_cost if pr.actual_cost is not None else 0
        
        total_expenditure = sum(get_cost(pr) for pr in prs)
        
        by_type = {}
        by_department = {}
        by_status = {}
        
        for pr in prs:
            cost = get_cost(pr)
            ptype = pr.purchase_type
            by_type[ptype] = by_type.get(ptype, 0) + cost
            
            dept = pr.department
            by_department[dept] = by_department.get(dept, 0) + cost
            
            status = pr.status
            by_status[status] = by_status.get(status, 0) + cost
        
        return jsonify({
            'totalExpenditure': total_expenditure,
            'byType': by_type,
            'byDepartment': by_department,
            'byStatus': by_status
        })
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
