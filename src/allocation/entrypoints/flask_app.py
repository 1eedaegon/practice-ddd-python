import config
from allocation.adapters import orm, repository
from allocation.domain import model
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(request.json["orderid"], request.json["sku"], request.json["qty"])
    batchref = model.allocate(line, batches)
    return jsonify({"batchref": batchref}, 201)
