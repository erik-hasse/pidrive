from concurrent import futures

import grpc

from pidrive.vehicles import PiCarV

import car_pb2
import car_pb2_grpc


class CarService(car_pb2_grpc.CarServicer):
    def __init__(self, car):
        self.car = car

    def move(self, request, context):
        self.car.velocity = request.velocity
        self.car.angle = request.angle
        return car_pb2.MoveReply()

    def image(self, request, context):
        frame = self.car.camera.read()
        return car_pb2.ImageReply(
            image_array=frame.tobytes(),
            shape=frame.shape,
            dtype=frame.dtype.str
        )

    def move_camera(self, request, context):
        getattr(self.car.camera, request.direction)(request.amount)
        return car_pb2.MoveCameraReply()


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    car_pb2_grpc.add_CarServicer_to_server(
        CarService(PiCarV()),
        server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
