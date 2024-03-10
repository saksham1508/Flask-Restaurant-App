from app import application
from flask import jsonify, Response, session
from app.models import *
from app import *
import uuid
import datetime
from marshmallow import Schema, fields
from flask_restful import Resource, Api
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import json

#  Restful way of creating APIs through Flask Restful
class SignUpAPI(MethodResource, Resource):
    @doc(description='Sign Up API', tags=['SignUp API'])
    @use_kwargs(SignUpRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            user = User(
                uuid.uuid4(),
                kwargs['username'],
                kwargs['password'],
                kwargs['name'],
                kwargs['user_id'],
                1,
                datetime.datetime.utcnow())
            db.session.add(user)
            db.session.commit()
            return APIResponse().dump(dict(message='User is successfully registered')), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to register user : {str(e)}')), 400


api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)

class LoginAPI(MethodResource, Resource):
    @doc(description='Login API', tags=['Login API'])
    @use_kwargs(LoginRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            user = User.query.filter_by(username=kwargs['username'], password=kwargs['password']).first()
            if user:
                print('logged in')
                session['user_id'] = user.user_id
                print(f'User id : {str(session["user_id"])}')
                return APIResponse().dump(dict(message='User is successfully logged in')), 200
                # return jsonify({'message':'User is successfully logged in'}), 200
            else:
                return APIResponse().dump(dict(message='User not found')), 404
                # return jsonify({'message':'User not found'}), 404
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to login user : {str(e)}')), 400


            

api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)

class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                session['user_id'] = None
                print('logged out')
                return APIResponse().dump(dict(message='User is successfully logged out')), 200
                # return jsonify({'message':'User is successfully logged out'}), 200
            else:
                print('user not found')
                return APIResponse().dump(dict(message='User is not logged in')), 401
                # return jsonify({'message':'User is not logged in'}), 401
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to logout user : {str(e)}')), 400
            

api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)


class AddVendorAPI(MethodResource, Resource):
    @doc(description='Add Vendors API', tags=['Add Vendors API'])
    @marshal_with(AddVendorsResponse)  # marshalling
    def post(self):
        if session['user_id']:
            vendors = vendors.query.filter_by(user_id=session['user_id'])
            vendors_list = list()
            for vendor in vendors:
                vendor_dict = {}
                vendor_dict['vendor_id'] = vendor.vendor_id
                vendor_dict['vendor_name'] = =vendor.vendor_name
                vendor_dict['item_description'] = vendor.item_description
                vendor_dict['balance_units'] = vendor.balance_units

                vendor_list.append(vendor_dict)
            print(vendor_list)
            return GetVendorsResponse().dump(dict(vendors=vendors_list)), 200

        except Exception as e:
        return APIResponse().dump(dict(message='Not able to add vendors')), 400


            

api.add_resource(AddVendorAPI, '/add_vendor')
docs.register(AddVendorAPI)


class GetVendorsAPI(MethodResource, Resource):
    @doc(description='Get Vendors API', tags=['Get Vendors API'])
    @marshal_with(GetVendorsResponse)  # marshalling
    def get(self):
        try:
            Vendors = vendors.query.all()
            vendors_list = list()
            for vendor in vendors:
                vendor_dict = {}
                vendor_dict['vendor_id'] = vendor.vendor_id
                vendor_dict['vendor_name'] = =vendor.vendor_name
                vendor_dict['item_description'] = vendor.item_description
                vendor_dict['balance_units'] = vendor.balance_units


                vendor_list.append(vendor_dict)
            print(vendor_list)
            return GetVendorsResponse().dump(dict(vendors=vendors_list)), 200

        except Exception as e:
            return APIResponse().dump(dict(message='Not able to list vendors')), 400


            

api.add_resource(GetVendorsAPI, '/list_vendors')
docs.register(GetVendorsAPI)

class AddItemAPI(MethodResource, Resource):
    @doc(description='Add Item API', tags=['Add Item API'])
    @use_kwargs(AddItemRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                user_id = kwargs['user_id']
            Vendors = vendors.query.all()
            vendors_list = list()
        if item_id <= 0:
            return APIResponse().dump(dict(message='Items must be more than 0.')), 400
            # return jsonify({'message':'Items must be more than 0.'}), 400
        Item = Items.query.filter_by(item_id=item_id, is_active=1).first()

        Item = Item(
            item_id=uuid.uuid4(),
            user_id=session['user_id'],
            vendor_id=vendor_id,
            item_name=item_name,
            calories_per_gm = calories_per_gm
            available_quantity = available_quantity
            restaurant_name = restaurant_name
            unit_price = unit_price
            is_active = 1
            created_ts=datetime.datetime.utcnow()
        )
        db.session.add(Item)

        items = Item.query.filter_by(user_id=session['user_id'], item_id=item_id).first()
        if not item_id:
            Item = Item(
                item_id=uuid.uuid4(),
                user_id=session['user_id'],
                vendor_id=vendor_id,
                item_name=item_name,
                calories_per_gm=calories_per_gm
                available_quantity = available_quantity
                restaurant_name = restaurant_name
                unit_price = unit_price
                is_active = 1
                created_ts = datetime.datetime.utcnow()
            )
            db.session.add(Item)
        else:
            Item.available_quantity = Item.available_quantity + available_quantity

        db.session.commit()

        return APIResponse().dump(dict(message='Item Added successfully ')), 200
        # return jsonify({'message':'Item Added successfully'}), 200

    else:
    print('Vendor not logged in')
    return APIResponse().dump(dict(message='Vendor is not logged in')), 401
    # return jsonify({'message':'User is not logged in'}), 401

except Exception as e:
print(str(e))
return APIResponse().dump(dict(message=f'Not able to add items : {str(e)}')), 400


            

api.add_resource(AddItemAPI, '/add_item')
docs.register(AddItemAPI)


class ListItemsAPI(MethodResource, Resource):
    @doc(description='List Items API', tags=['List Items API'])
    @marshal_with(ListItemsResponse)  # marshalling
    def get(self):
        try:
            Item = Item.query.all()
            Item_list = list()
            for item in items:
                item_dict = {}
                item_dict['item_id'] = item.item_id
                item_dict['vendor_name'] = =item.vendor_name
                item_dict['item_description'] = item.item_description
                item_dict['available_quantity'] = item.available_quantity


                item_list.append(item_dict)
            print(item_list)
            return ListItemsResponse().dump(dict(item=item_list)), 200

        except Exception as e:
            return APIResponse().dump(dict(message='Not able to list items')), 400

api.add_resource(ListItemsAPI, '/list_items')
docs.register(ListItemsAPI)


class CreateItemOrderAPI(MethodResource, Resource):
    @doc(description='Create Item Order API', tags=['Create Item Order API'])
    @use_kwargs(CreateItemOrder, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                user_id = kwargs['user_id']
            Vendors = vendors.query.all()
            vendors_list = list()
        if item_id <= 0:
            return APIResponse().dump(dict(message='Items must be more than 0.')), 400
            # return jsonify({'message':'Items must be more than 0.'}), 400
        OrderItems = OrderItems.query.filter_by(item_id=item_id, is_active=1).first()

        OrderItems = OrderItems(
            id = id
            order_id = order_id
            item_id = item_id
            quantity = quantity
            is_active = 1
            created_ts = datetime.utcnow()
        )
        db.session.add(OrderItems)

        OrderItems = OrderItems.query.filter_by(user_id=session['user_id'], item_id=item_id).first()
        if not item_id:
            OrderItems = OrderItems(
                id=id
                order_id = order_id
                item_id = item_id
                quantity = quantity
                is_active = 1
                created_ts = datetime.utcnow()
            )
            db.session.add(Item)
        else:
            OrderItems.quantity = OrderItems.quantity + quantity

        db.session.commit()

        return APIResponse().dump(dict(message='Order Item successful ')), 200
        # return jsonify({'message':'Item Added successfully'}), 200

    else:
    print('Vendor not logged in')
    return APIResponse().dump(dict(message='Vendor is not logged in')), 401
    # return jsonify({'message':'User is not logged in'}), 401

except Exception as e:
print(str(e))
return APIResponse().dump(dict(message=f'Not able to order items : {str(e)}')), 400

            

api.add_resource(CreateItemOrderAPI, '/create_items_order')
docs.register(CreateItemOrderAPI)


class PlaceOrderAPI(MethodResource, Resource):
    @doc(description='Place Order API', tags=['Place Order API'])
    @use_kwargs(PlaceOrder, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                user_id = kwargs['user_id']
        if item_id <= 0:
            return APIResponse().dump(dict(message='Items must be more than 0.')), 400
            # return jsonify({'message':'Items must be more than 0.'}), 400
        Order = Order.query.filter_by(item_id=item_id, is_active=1).first()

        Order = Order(
            order_id = order_id
            user_id = user_id
            total_amount = 0
            is_active = 1
            created_ts = datetime.utcnow()
        )
        db.session.add(Order)

        Order = Order.query.filter_by(user_id=session['user_id'], item_id=item_id).first()
        if not order_id:
            Order = Order(
            order_id=order_id
            user_id = user_id
            total_amount = 0
            is_active = 1
            created_ts = datetime.utcnow()
            )

            db.session.add(Order)
        else:
            Order.total_amount = Order.total_amount + total_amount

        db.session.commit()

        return APIResponse().dump(dict(message='Order successful ')), 200
        # return jsonify({'message':'Item Added successfully'}), 200

    else:
    print('Customer not logged in')
    return APIResponse().dump(dict(message='Customer is not logged in')), 401
    # return jsonify({'message':'User is not logged in'}), 401

except Exception as e:
print(str(e))
return APIResponse().dump(dict(message=f'Not able to order : {str(e)}')), 400
            

api.add_resource(PlaceOrderAPI, '/place_order')
docs.register(PlaceOrderAPI)

class ListOrdersByCustomerAPI(MethodResource, Resource):
    @doc(description='List Items By Customer API', tags=['List Items by Customer API'])
    @marshal_with(ListItemsCustomerResponse)  # marshalling
    def get(self):
        try:
            Order = Order.query.all()
            Order_list = list()
            for Order in Order:
                order_dict = {}
                order_dict['order_id'] = order.order_id
                order_dict['user_id'] = =order.user_id
                order_dict['total_amount'] = order.total_amount


                order_list.append(order_dict)
            print(order_list)
            return ListItemsCustomerResponse().dump(dict(order=order_list)), 200

        except Exception as e:
            return APIResponse().dump(dict(message='Not able to list Customer Orders')), 400

            

api.add_resource(ListOrdersByCustomerAPI, '/list_orders')
docs.register(ListOrdersByCustomerAPI)


class ListAllOrdersAPI(MethodResource, Resource):
    @doc(description='List All Orders API', tags=['List All Orders API'])
    @marshal_with(ListAllOrdersResponse)  # marshalling
    def get(self):
        try:
            OrderItems = OrderItems.query.all()
            OrderItems_list = list()
            for OrderItem in OrderItems:
                orderItem_dict = {}
                orderItem_dict['order_id'] = orderItem.order_id
                orderItem_dict['Item_id'] = =orderItem.item_id
                orderItem_dict['Quantity'] = orderItem.Quantity

                orderItem_list.append(orderItem_dict)
            print(orderItem_list)
            return OrderItemsListResponse().dump(dict(orderItem=orderItem_list)), 200

        except Exception as e:
            return APIResponse().dump(dict(message='Not able to list All Orders')), 400

            
api.add_resource(ListAllOrdersAPI, '/list_all_orders')
docs.register(ListAllOrdersAPI)