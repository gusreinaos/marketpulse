//Author: John Berntsson
import React from 'react';
import { Container, Row, Col, Card, Button, InputGroup, FormControl, ProgressBar } from 'react-bootstrap';

const ProfilePage = () => {
  return (
    <Container>
      <div className="main-body">
        <Row>
          <Col lg={4}>
            <Card>
              <Card.Body>
                <div className="d-flex flex-column align-items-center text-center">
                  <img
                    src="https://bootdey.com/img/Content/avatar/avatar6.png"
                    alt="Admin"
                    className="rounded-circle p-1 bg-primary"
                    width="110"
                  />
                  <div className="mt-3">
                    <h4>John Doe</h4>
                    <p className="text-secondary mb-1">Full Stack Developer</p>
                    <p className="text-muted font-size-sm">Bay Area, San Francisco, CA</p>
                    <Button variant="primary">Follow</Button>
                    <Button variant="outline-primary" className="ms-2">
                      Message
                    </Button>
                  </div>
                </div>
                <hr className="my-4" />
                <ul className="list-group list-group-flush">
                  <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                    <h6 className="mb-0">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="feather feather-globe me-2 icon-inline"
                      >
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="2" y1="12" x2="22" y2="12"></line>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                      </svg>
                      Website
                    </h6>
                    <span className="text-secondary">https://bootdey.com</span>
                  </li>
                  {/* Other list items go here */}
                </ul>
              </Card.Body>
            </Card>
          </Col>
          <Col lg={8}>
            {/* Other content goes here */}
          </Col>
        </Row>
      </div>
    </Container>
  );
};

export default ProfilePage;
